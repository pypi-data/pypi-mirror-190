from __future__ import annotations

import functools
import logging
import pathlib
import subprocess
from concurrent.futures import ThreadPoolExecutor
from time import sleep

from me_setups.components.eqs import EyeQ5
from me_setups.components.eqs import OSType
from me_setups.components.mcu import Mcu

from me_deploy.uboot.from_linux import check_uboot

XMODEM_CMD = "sx -C 4 {filename} > {port} < {port}"
UBOOT_FILES = {
    "BOOTMGR": "bootmgr.bin",
    "MI": "miv1_c{chip}d{mid}.bin",
    "DDRFW": "ddrfw.bin",
    "UBOOT": "uboot.bin",
}


logger = logging.getLogger("XMODEM")


def xmodem(
    files_folder: pathlib.Path,
    uboot_file: str,
    eq: EyeQ5,
    log_folder: pathlib.Path,
    timeout: float = 300,
) -> EyeQ5 | None:
    uboot_fullname = uboot_file.format(chip=eq.chip, mid=eq.mid)
    filename = files_folder / uboot_fullname
    eq.logger.debug(f"[start] sending {filename.name!r}")
    cmd = XMODEM_CMD.format(filename=filename, port=eq.serial.port)
    log_folder = log_folder / eq.name
    log_folder.mkdir(parents=True, exist_ok=True)
    with (log_folder / f"{filename.stem}.log").open("w", buffering=1) as f:
        try:
            subprocess.check_call(
                cmd,
                shell=True,
                stdout=f,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                timeout=timeout,
            )
        except subprocess.CalledProcessError:
            logger.exception(
                f"sending {uboot_fullname} XMODEM to {eq} failed!",
            )
            return None
    eq.logger.debug(f"[end] sending {filename.name}")
    return eq


def move_to_xmodem(eqs: list[EyeQ5], mcu: Mcu) -> None:
    if not eqs:
        return None
    logger.info("setting eqs to xmodem")
    for eq in eqs:
        set_eq_to_xmodem(mcu, eq)


def set_eq_to_xmodem(mcu: Mcu, eq: EyeQ5) -> None:
    mcu.logger.debug(f"setting {eq} to xmodem")
    mcu_eq_name = mcu.get_eq_name(eq)
    eq.serial.reset_output_buffer()
    mcu.run_serial_cmd(f"set {mcu_eq_name} bootmode xmodem")
    mcu.run_serial_cmd(f"reset {mcu_eq_name}")
    assert eq_in_xmodem(eq)
    eq.logger.debug("On XMODEM")


def eq_in_xmodem(eq: EyeQ5) -> bool:
    XMODEM_EXP = b"XMODEM transfer started. Please send your file now.\r\n\x15"
    with eq.change_timeout_ctx(30):
        return XMODEM_EXP in eq.serial.read_until(XMODEM_EXP)


def send_file(
    eq: EyeQ5,
    files_folder: pathlib.Path,
    uboot_file: str,
    log_folder: pathlib.Path,
) -> EyeQ5 | None:
    eq.serial.read(eq.serial.in_waiting)
    eq.serial.read_until(b"\x15")
    eq_success = xmodem(files_folder, UBOOT_FILES[uboot_file], eq, log_folder)
    if uboot_file != "UBOOT":
        READY = b"XMODEM is ready"
        assert READY in eq.serial.read_until(READY)
        eq.os_type = OSType.UBOOT
    else:
        check_uboot(eq, set_code=False)
    eq.serial.close()
    sleep(0.1)
    eq.serial.open()
    return eq_success


def xmodem_to_uboot(
    eqs: list[EyeQ5],
    files_folder: pathlib.Path,
    log_folder: pathlib.Path,
) -> list[EyeQ5]:
    if not eqs:
        return []
    for uboot_file in UBOOT_FILES:
        logger.info(f"[start] sending {uboot_file}.")
        with ThreadPoolExecutor(max_workers=len(eqs)) as ex:
            eq_success = ex.map(
                functools.partial(
                    send_file,
                    files_folder=files_folder,
                    uboot_file=uboot_file,
                    log_folder=log_folder / "XMODEM",
                ),
                eqs,
            )
        eqs = [eq for eq in eq_success if eq is not None]
        logger.info(f"[end] sending {uboot_file}.")
    return eqs
