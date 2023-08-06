from __future__ import annotations

import logging
import pathlib

from me_setups.components.eqs import EyeQ5
from me_setups.components.mcu import Mcu

from me_deploy.uboot.from_linux import uboot_from_linux
from me_deploy.uboot.xmodem import move_to_xmodem
from me_deploy.uboot.xmodem import xmodem_to_uboot

logger = logging.getLogger(__name__)


def load_uboot(
    eqs: list[EyeQ5],
    mcu: Mcu,
    log_folder: pathlib.Path,
    files_folder: pathlib.Path,
) -> set[EyeQ5]:
    uart_log_folder: pathlib.Path = log_folder / "UART_logs"

    for eq in eqs:
        eq.config_serial_log_file(uart_log_folder / f"{eq.name}.log")
    mcu.config_serial_log_file(uart_log_folder / f"{mcu.name}.log")

    eqs_set = set(eqs)

    eqs_on_uboot: set[EyeQ5]
    try:
        eqs_on_uboot = set(uboot_from_linux(mcu, eqs))
    except AssertionError:
        eqs_on_uboot = set()
        logger.warning("Mcu is not supporting load from Linux")

    eqs = list(eqs_set - eqs_on_uboot)

    move_to_xmodem(eqs, mcu)
    return eqs_on_uboot | set(
        xmodem_to_uboot(
            eqs,
            files_folder,
            log_folder,
        ),
    )
