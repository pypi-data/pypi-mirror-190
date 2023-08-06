from __future__ import annotations

import logging
import pathlib

import psutil

from me_deploy.constants import RESOURCES_DIR
from me_deploy.tools import power_cycle
from me_deploy.tools import run_on_linux

MARVELL = RESOURCES_DIR / "marvell"
OFFICIAL_FW = MARVELL / "official_fw"
MRVL_BIN = MARVELL / "mrvl88q_bin"
UPLOAD_TOOL = MRVL_BIN / "mrvl88q_unified_upload.s5"
TIMEOUT = 30
CMD = f"sudo timeout {TIMEOUT} {UPLOAD_TOOL}"

logger = logging.getLogger(__name__)

supported_ver = {
    "factory_image": "88Q6113_flash_0.07.1186_patched.bin",
    "v10": "GAS52_88Q6113_flash_210905_v10.bin",
    "v11": "GAS52_88Q6113_flash_211111_v11.bin",
    "v15": "GAS52_88Q6113_flash_220224_v15.bin",
    "v16": "GAS52_88Q6113_flash_220508_v16.bin",
    "v17": "GAS52_88Q6113_flash_220607_v17.bin",
    "v18": "GAS52_88Q6113_flash_220711_v18.bin",
}


def get_ip_interface_name(ip: str) -> str:
    for interface, snicaddrs in psutil.net_if_addrs().items():
        if ip in [snicaddr.address for snicaddr in snicaddrs]:
            return interface
    raise ValueError(f"ip {ip} not found! Check if it exists: `ip a`")


def switch_upload(
    switch_ver: str,
    log_folder: pathlib.Path | None,
    *,
    skip_power_cycle: bool = False,
) -> None:
    try:
        switch_file = OFFICIAL_FW / switch_ver / supported_ver[switch_ver]
    except KeyError:
        logger.error(f"version {switch_file} is not supported!")
        raise
    logger.info(f"flashing switch file: {switch_file.name}")
    interface = get_ip_interface_name("198.18.32.1")
    run_on_linux(
        f"{CMD} {interface}:{switch_file}:t,f,c",
        f"flash_{switch_ver}",
        log_folder,
        check=True,
    )
    logger.info(f"flashing file: {switch_file.name} - success")
    if not skip_power_cycle:
        power_cycle(sleep_after=45)
