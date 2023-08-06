from __future__ import annotations

import logging
import pathlib
import sys
import time

from me_setups.boards.gas52 import Gas52Board
from me_setups.components.mcu import Mcu
from me_setups.components.mcu import McuType

from me_deploy.constants import RESOURCES_DIR
from me_deploy.tools import power_cycle
from me_deploy.tools import run_on_linux

MCU_TOOLS = pathlib.Path(__file__).parent / "mcu_tools"
CLI_SHELL_PATH = "flashing/cli_shell.py"
FLASH_WINE_PATH = "ci_flashing/board_flash_wine.py"
GAS52_MEAVES_FILE = {
    McuType.MEAVES: "mcu_meaves_gas52_eol.hex",
    McuType.MEAVES_SINGLE_IMG: "GAS52_EVO_MCU_V2R2_single_image.hex",
}
MCU_RESOURCES = RESOURCES_DIR / "mcu"


logger = logging.getLogger(__name__)


def memtool_mcu_flash(
    mcu: Mcu,
    log_folder: pathlib.Path,
    mcu_type: McuType,
    *,
    skip_power_cycle: bool = False,
) -> None:
    log_folder = log_folder / "MEMTOOL_MEAVES"
    mcu_file = MCU_RESOURCES / GAS52_MEAVES_FILE[mcu_type]
    log_folder.mkdir(parents=True, exist_ok=True)
    run_on_linux("pkill DAS", "kill_DAS_server")
    run_on_linux("pkill IMTMemtool.exe", "kill_Memtool_windows_app")
    flash_wine_path = MCU_TOOLS / FLASH_WINE_PATH
    cmd = f"{sys.executable} {flash_wine_path} -i {mcu_file} -b GAS"
    run_on_linux(cmd, "memtool_process", log_folder, check=True)
    if not skip_power_cycle:
        mcu.config_serial_log_file(log_folder / "mcu_uart.log")
        power_cycle()
        mcu.run_serial_cmd("info")
        mcu.serial.read_all()
    logger.info(f"setting MCU type to: {mcu_type}")
    mcu.mcu_type = mcu_type


def deploy_meaves_to_asr(
    board: Gas52Board,
    mcu_version: str = "GAS52EVO_DC1E-A_22.12.RC",
    sleep_after: float = 60,
) -> None:
    mcu = board.mcu
    logger.info("converet MCU from MEAVES to ASR")
    mcu.run_serial_cmd("power ALL off")
    mcu.serial.read_until(mcu.prompt)
    mcu.run_serial_cmd("test flash d PF4 R")
    logger.info(f"sleeping for {sleep_after} seconds...")
    time.sleep(sleep_after)
    power_cycle()
    mcu.mcu_type = McuType.ASR
    board.restart_serials()
    mcu.run_serial_cmd("version -v")
    data = mcu.serial.read_all().decode()
    logger.debug(f"MCU data read:\n{data}")
    assert mcu_version in data
    logger.info("converet MCU from MEAVES to ASR - success")


def deploy_meaves_to_adam(
    board: Gas52Board,
    m2a_log_folder: pathlib.Path,
    mcu_image_file: pathlib.Path | None,
    mcu_bl_file: pathlib.Path | None,
    *,
    run_power_cycle: bool = True,
) -> None:
    m2a_log_folder = m2a_log_folder / "MEAVES_TO_ADAM"
    ip, port = board.mcu.address
    cli_shell_path = MCU_TOOLS / CLI_SHELL_PATH
    cmd = f"{sys.executable} {cli_shell_path} -U {ip}:{port}"
    img_cmd = f'-c "netflash_mcu 4567 1280" -f {mcu_image_file}'
    image_log_folder = m2a_log_folder / "image"
    board.mcu.config_serial_log_file(image_log_folder / "mcu_uart.log")
    run_on_linux(
        f"{cmd} {img_cmd}",
        "process",
        image_log_folder,
        check=True,
    )
    time.sleep(5)
    board.mcu.serial.read_all()
    bl_cmd = f'-c "netflash_hex 4567 1280" -f {mcu_bl_file}'
    bl_log_folder = m2a_log_folder / "bootloader"
    board.mcu.config_serial_log_file(bl_log_folder / "mcu_uart.log")
    run_on_linux(
        f"{cmd} {bl_cmd}",
        "process",
        bl_log_folder,
        check=True,
    )
    time.sleep(5)
    board.mcu.serial.read_all()

    if run_power_cycle:
        power_cycle(30, 30)

    board.mcu.mcu_type = McuType.ADAM
    ip, port = board.mcu.address
    confirm_cmd = f'-c "netflash_confirm"'
    confirm_log_folder = m2a_log_folder / "confirm"
    board.mcu.config_serial_log_file(confirm_log_folder / "mcu_uart.log")
    run_on_linux(
        f"{cmd} {confirm_cmd}",
        "process",
        confirm_log_folder,
    )
    time.sleep(5)
    board.mcu.serial.read_all()
