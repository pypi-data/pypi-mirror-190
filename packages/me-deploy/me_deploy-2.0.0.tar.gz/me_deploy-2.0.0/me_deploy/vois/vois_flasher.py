from __future__ import annotations

import logging
import pathlib
import shutil
from concurrent.futures import ThreadPoolExecutor
from time import sleep

import psutil
from me_setups.components.eqs import EyeQ5
from me_setups.components.eqs import OSType
from me_setups.components.mcu import Mcu
from me_setups.components.tools import get_eq_ip

logger = logging.getLogger("VOIS flash")

VOIS_DIR = "files"

EQ5_IPS = {
    "EQ5_PBCM_0000": "192.168.19.129",
    "EQ5_PBCM_0001": "192.168.19.113",
    "EQ5_PBCM_0010": "192.168.19.105",
    "EQ5_PBCM_0011": "192.168.19.121",
}


def get_server_ip(subnet: str) -> str:
    for snicaddrs in psutil.net_if_addrs().values():
        for snicaddr in snicaddrs:
            if subnet in snicaddr.address:
                return snicaddr.address
    raise ValueError(f"Subnet {subnet} not found! Check if it exists: `ip a`")


class VoisFlasher:
    def __init__(self, eq: EyeQ5) -> None:
        self.eq = eq
        self.ip = get_eq_ip(self.eq.name, OSType.LINUX)
        self.server_ip = get_server_ip("192.168.19")

    def uboot_run_cmd(
        self,
        cmd: str,
        expected: bytes | None = None,
        sleep_before_read: float = 0.0,
    ) -> bytes:
        self.eq.run_serial_cmd(cmd)
        sleep(sleep_before_read)
        if expected is None:
            return self.eq.serial.read_until(self.eq.prompt)
        else:
            return self.eq.serial.read_until(expected)

    def tftp_file(self, filename: str) -> bool:
        expected = b"done"
        response = self.uboot_run_cmd(
            f"tftp ${{loadaddr}} {VOIS_DIR}/{filename}",
            expected=expected,
        )
        return self.check_in_response(expected, response)

    def mmc_write(self, start_block: int, blocks_to_write: int) -> bool:
        expected = b"blocks written: OK"
        response = self.uboot_run_cmd(
            f"mmc write ${{loadaddr}} {start_block} {blocks_to_write}",
            expected=expected,
        )
        return self.check_in_response(expected, response)

    def tftp_and_write(
        self,
        filename: str,
        start_block: int,
        blocks_to_write: int,
    ) -> bool:
        return self.tftp_file(filename) and self.mmc_write(
            start_block,
            blocks_to_write,
        )

    def pre_vois(self) -> bool:
        self.eq.serial.reset_input_buffer()
        self.eq.serial.reset_output_buffer()
        self.eq.run_serial_cmd("\n")
        self.eq.serial.read_until(self.eq.prompt)

        self.config_sysparms()
        self.mmc_config()

        return all(
            [
                # erase boot part
                self.switch_to_dev(1),
                self.mmc_erase(0, 20000),
                # erase user part
                self.switch_to_dev(0),
                self.mmc_erase(0, 100000),
            ],
        )

    def mmc_erase(self, start_block: int, blocks_to_erase: int) -> bool:
        expected = b"blocks erased: OK"
        response = self.uboot_run_cmd(
            f"mmc erase {start_block} {blocks_to_erase}",
            expected=expected,
            sleep_before_read=5,
        )
        return self.check_in_response(expected, response)

    def switch_to_dev(self, dev_part: int) -> bool:
        expected = bytes(
            f"(part {dev_part}) is current device",
            encoding="utf-8",
        )
        response = self.uboot_run_cmd(
            f"mmc dev 0 {dev_part}",
            expected=expected,
        )
        return self.check_in_response(expected, response)

    def mmc_config(self) -> None:
        self.uboot_run_cmd("mmc bootbus 0 2 1 2")
        self.uboot_run_cmd("mmc partconf 0 0 1 0")
        self.uboot_run_cmd("mmc rst-function 0 1")

    def config_sysparms(self) -> None:
        self.uboot_run_cmd("env default -a")
        self.uboot_run_cmd(f"setenv ipaddr {self.ip}")
        self.uboot_run_cmd(f"setenv serverip {self.server_ip}")
        self.uboot_run_cmd("setenv loadaddr 0x9000000810000000")
        self.uboot_run_cmd("saveenv")

    def flash_user_part(self) -> bool:
        if not self.switch_to_dev(0):
            return False
        tftp_commands = [
            ("fpd_emmc.bin", 100, 2),
            ("boot_manager.for_tests.UNIFIED.ddrfw.bin", 200, 300),
            ("VOIS.dram_elfload.hex.bin", 1000, 2500),
            ("vois_tests_fat.vhd", 800000, 20000),
            ("platformConfig_GAS52", 190000, 60),
        ]
        for cmd in tftp_commands:
            if not self.tftp_and_write(*cmd):
                return False

        return True

    def flash_boot_part(self) -> bool:
        return self.switch_to_dev(1) and self.tftp_and_write(
            "boot_manager.for_tests.UNIFIED.bin",
            0,
            100,
        )

    def mi_flash(self) -> bool:
        sleep(3)  # workaround for issue: "Error: card/blk is write protected!"
        if not self.tftp_file(
            f"miv1_voisparams_c{self.eq.chip}d{self.eq.mid}.bin",
        ):
            return False
        assert self.switch_to_dev(0)
        expected = b"mi write finished successfully"
        response = self.uboot_run_cmd(
            "mi bwrite ${loadaddr} --force_media=emmc",
            expected=expected,
        )
        return self.check_in_response(
            expected,
            response,
        )

    def run(self) -> EyeQ5 | None:
        if not self.pre_vois():
            return None
        if not self.flash_user_part():
            return None
        if not self.flash_boot_part():
            return None
        if not self.mi_flash():
            return None
        self.eq.serial.read_until(self.eq.prompt)
        return self.eq

    @staticmethod
    def check_in_response(check: bytes, response: bytes) -> bool:
        result = check in response
        if not result:
            logger.warning(f"{check.decode()!r} not in:\n{response.decode()}")
        return result


def run_vois(eq: EyeQ5) -> EyeQ5 | None:
    return VoisFlasher(eq).run()


def flash_eqs(
    eqs: list[EyeQ5],
    mcu: Mcu,
    log_folder: pathlib.Path,
    tftp_folder: pathlib.Path,
    files_folder: pathlib.Path,
    *,
    reset_after: bool = True,
) -> list[EyeQ5]:
    assert tftp_folder and files_folder
    logger.info("[start] flashing VOiS. this can take a few min...")
    uart_log_folder: pathlib.Path = log_folder / "UART_logs"
    uart_log_folder.mkdir(parents=True, exist_ok=True)

    for eq in eqs:
        eq.config_serial_log_file(uart_log_folder / f"{eq.name}.log")
    mcu.config_serial_log_file(uart_log_folder / f"{mcu.name}.log")
    eqs_success = []
    tftp_files_folder = tftp_folder / VOIS_DIR
    shutil.copytree(files_folder, tftp_files_folder, dirs_exist_ok=True)
    with ThreadPoolExecutor(max_workers=len(eqs)) as ex:
        results = ex.map(run_vois, eqs)
    eqs_success = [eq for eq in results if eq is not None]
    for eq in eqs_success:
        eq.os_type = OSType.VOIS
    if len(eqs_success) == 4:
        mcu.set_eq_bootmode("all", "emmc")
        mcu.set_eq_uboot("all", "off")
    else:
        for eq in eqs_success:
            mcu.set_eq_bootmode(eq, "emmc")
            mcu.set_eq_uboot(eq, "off")
    if reset_after:
        if len(eqs_success) == 4:
            mcu.reset_eq("all")
        else:
            for eq in eqs_success:
                mcu.reset_eq(eq)
    logger.info("[end] flashing VOiS.")
    shutil.rmtree(tftp_files_folder)
    return eqs_success
