from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor

from me_setups.components.eqs import EyeQ5
from me_setups.components.eqs import OSType
from me_setups.components.eqs import PROMPTS
from me_setups.components.mcu import Mcu
from me_setups.components.mcu import McuType

logger = logging.getLogger(__name__)


def uboot_from_linux(mcu: Mcu, eqs: list[EyeQ5]) -> list[EyeQ5]:
    assert mcu.mcu_type in (
        McuType.ADAM,
        McuType.MEAVES,
        McuType.MEAVES_SINGLE_IMG,
    )
    logger.info("moving to U-boot from Linux")
    for eq in eqs:
        mcu.set_eq_bootmode(eq, "emmc")
        mcu.set_eq_uboot(eq, "on")
        mcu.reset_eq(eq)
    with ThreadPoolExecutor(max_workers=len(eqs)) as ex:
        eq_success = ex.map(check_uboot, eqs)
    eqs_on_uboot = [eq for eq in eq_success if eq is not None]
    eqs_not_on_uboot = set(eqs) - set(eqs_on_uboot)
    if eqs_not_on_uboot:
        logger.warning(f"Not all eqs on U-boot: {eqs_not_on_uboot}")
    return eqs_on_uboot


def check_uboot(eq: EyeQ5, *, set_code: bool = True) -> EyeQ5 | None:
    try:
        if set_code:
            eq.serial.read_until(b"press <q> to abort")
            eq.run_serial_cmd("q")
        prompt = PROMPTS[OSType.UBOOT]
        assert prompt in eq.serial.read_until(prompt)
        eq.logger.info("On U-boot")
        eq.os_type = OSType.UBOOT
        return eq
    except AssertionError:
        return None
