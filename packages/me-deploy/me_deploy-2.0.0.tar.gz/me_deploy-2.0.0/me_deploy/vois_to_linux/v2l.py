from __future__ import annotations

import functools
import hashlib
import json
import logging
import math
import os
import pathlib
import re
import select
import socket
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from io import TextIOWrapper

from me_setups.components.eqs import EyeQ5
from me_setups.components.eqs import OSType
from me_setups.components.mcu import Mcu

from me_deploy.vois_to_linux import models


VOIS_ADDRESS = ("169.254.0.2", 24000)
EQ_TO_VOIS_IP = {
    "EQ5_PBCM_0000": "169.254.0.11",
    "EQ5_PBCM_0001": "169.254.0.12",
    "EQ5_PBCM_0010": "169.254.0.13",
    "EQ5_PBCM_0011": "169.254.0.14",
}
EQ_TO_LINUX_IP = {
    "EQ5_PBCM_0000": "192.168.19.129",
    "EQ5_PBCM_0001": "192.168.19.113",
    "EQ5_PBCM_0010": "192.168.19.105",
    "EQ5_PBCM_0011": "192.168.19.121",
}
ADDR_TO_EQ = {value: key for key, value in EQ_TO_VOIS_IP.items()}
HEX_PATTERN = re.compile(rb"0x([a-fA-F0-9]+)")
FLASH_SIZE_PATTERN = re.compile(rb"Size \(MB\): (\d+)")


logger = logging.getLogger("VOiS to Linux")


def extract_to_tftp(
    zip_image_path: pathlib.Path,
    tftp_path: pathlib.Path,
    eqs: list[EyeQ5],
) -> dict[str, models.Component]:
    eq_names = {eq.name for eq in eqs}
    with zipfile.ZipFile(zip_image_path) as zf:
        logger.debug("opening fota_manifest")
        with zf.open("fota_manifest.json") as f:
            fota_manifest = models.FotaManifest(**(json.load(f)))
        logger.debug("getting components")
        eq_components: dict[str, models.Component] = {
            component.id: component
            for component in fota_manifest.components
            if component.type == "EQ5" and component.id in eq_names
        }
        logger.debug("extracting EQs files to tftp")
        for eq_component in eq_components.values():
            with zipfile.ZipFile(zf.open(eq_component.filename)) as eq_zf:
                eq_zf.extractall(tftp_path)
        if "userpart_mbe.bin" in zf.namelist():
            logger.debug("extracting userpart_mbe file to tftp")
            zf.extract("userpart_mbe.bin", tftp_path)
    return eq_components


def get_v2l_sockets(mcu: Mcu, eqs: list[EyeQ5]) -> dict[str, socket.socket]:
    expected_clients = {eq.ip for eq in eqs}
    clients: dict[str, socket.socket] = {}
    with socket.socket() as sock:
        sock.bind(VOIS_ADDRESS)
        sock.listen(10)
        sock.settimeout(5.0)
        mcu.reset_eq("all")
        addresses: set[str] = set()
        while expected_clients - addresses:
            try:
                client, address = sock.accept()
            except KeyboardInterrupt:
                break
            else:
                if (
                    address[0] not in addresses
                    and address[0] in expected_clients  # format
                ):
                    addresses.add(address[0])
                    clients[ADDR_TO_EQ[address[0]]] = client
                    logger.info(f"Client connected - {address}")
    return clients


def validate_linux(eq: EyeQ5, board_name: str, board_rev: str) -> bool:
    proc = eq.run_ssh_cmd("cat /sys/kernel/manu_info/mi_value")
    return (
        f'board_name = "{board_name}"' in proc.stdout
        and f"board_rev = {board_rev}" in proc.stdout
    )


def md5(filename: pathlib.Path) -> str:
    with filename.open("rb") as f:
        return hashlib.md5(f.read()).hexdigest()


class V2LEyeQ:
    tftp_folder: pathlib.Path
    eq_socket: socket.socket
    eq_component: models.Component

    def __init__(
        self,
        eq: EyeQ5,
        eq_socket: socket.socket,
        eq_component: models.Component,
        tftp_folder: pathlib.Path,
        log_file: TextIOWrapper | None = None,
    ) -> None:
        self.eq = eq
        self.eq_socket = eq_socket
        self.eq_socket.settimeout(100.0)
        self.tftp_folder = tftp_folder
        self.eq_component = eq_component
        self.name = eq_component.id
        self.flash_size: int | None = None
        self.logger = logging.getLogger(self.name)
        if log_file is None:
            self.log_file = open(os.devnull, "w", buffering=1)
        else:
            self.log_file = log_file

    def validate_md5(
        self,
        f_path: pathlib.Path,
        offset: str,
        size: str,
    ) -> None:
        response = self.send_cmd(f"emmc md5 {offset} {size}")
        eq_md5s = [a.zfill(8) for a in HEX_PATTERN.findall(response)[-4:]]
        eq_file_md5 = b"".join(eq_md5s).decode()
        assert eq_file_md5 == md5(f_path)

    def get_flash_size(self) -> None:
        response = self.send_cmd(cmd="emmc info size")
        match = FLASH_SIZE_PATTERN.search(response)
        if match:
            self.flash_size = int(match.group(1)) * (1024**2)
            self.logger.debug(f"flash size is {self.flash_size}")

    def recv_all(self) -> bytes:
        line = bytearray()
        while True:
            r, _, _ = select.select([self.eq_socket], [], [], 3.0)
            if self.eq_socket in r:
                chunk = self.eq_socket.recv(1024)
                line += chunk
                time.sleep(0.01)
            else:
                break
        self.log_file.write(line.decode())
        return bytes(line)

    def send_cmd(self, cmd: str, sleep_before_recv: float = 0.4) -> bytes:
        self.logger.debug(f"running cmd: {cmd!r}")
        bytes_cmd = bytearray(f"{cmd}\r\n", encoding="utf-8")
        self.eq_socket.sendall(bytes_cmd)
        time.sleep(sleep_before_recv)
        return self.recv_all()

    def tftp_transfer(self, tftp_path: pathlib.Path) -> None:
        response = self.send_cmd(f"tftp 0x804000000 {tftp_path}")
        assert b"Bytes transferred" in response

    def emmc_write(self, offset: str, size: str) -> None:
        response = self.send_cmd(
            f"emmc write {offset} 0x804000000 {size}",
            sleep_before_recv=10,
        )
        assert b"completed successfully" in response

    def write_action(self, action: models.Action) -> None:
        assert self.flash_size, f"Could not get flash size for {self.name}"
        if action.part == "switch":
            return None
        tftp_folder = self.tftp_folder
        if action.file_name == "userpart_mbe.bin":
            f_path = tftp_folder / action.file_name
        else:
            f_path = tftp_folder / self.eq_component.id / action.file_name
        offset = action.offset
        if not offset:
            offset = hex(0)
        elif int(offset, 0) < 0:
            offset = hex((self.flash_size + int(offset, 16)) // 0x200)
        else:
            offset = hex(int(offset, 16) // 0x200)

        size = hex(math.ceil(f_path.stat().st_size / 0x200))

        if action.file_name == "userpart_mbe.bin":
            tftp_path = pathlib.Path(action.file_name)
        else:
            tftp_path = pathlib.Path(self.eq_component.id) / action.file_name

        if action.file_name == "userpart_mbe.bin":
            if action.action == "download":
                self.send_cmd(f"emmc setpart {action.part}")
                self.tftp_transfer(tftp_path)
            elif action.action == "burn":
                self.emmc_write(offset, size)
        else:
            self.send_cmd(f"emmc setpart {action.part}")
            self.tftp_transfer(tftp_path)
            self.emmc_write(offset, size)
        if action.action == "OS":
            self.validate_md5(f_path, offset, size)

    def flash_eq(self) -> None:
        tftp_folder = self.tftp_folder

        self.logger.info(
            "[start] moving from VOiS to Linux this may take a few minutes...",
        )
        self.get_flash_size()
        with open(tftp_folder / self.name / "agent_manifest.json") as f:
            agent_manifest = models.AgentManifest(**(json.load(f)))
        for action in agent_manifest.actions:
            self.write_action(action)
        self.eq.os_type = OSType.LINUX
        self.log_file.close()
        self.logger.info("[end] moving from VOiS to Linux")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"


def flash(
    eqs: list[EyeQ5],
    mcu: Mcu,
    log_folder: pathlib.Path,
    tftp_folder: pathlib.Path | None,
    zip_image_path: pathlib.Path | None,
    board_name: str,
    board_rev: str,
) -> None:
    assert tftp_folder and zip_image_path
    socket_log_folder: pathlib.Path = log_folder / "socket_logs"
    socket_log_folder.mkdir(parents=True, exist_ok=True)
    for eq in eqs:
        mcu.set_eq_uboot(eq, "off")
        mcu.set_eq_bootmode(eq, "emmc")
    eq_components = extract_to_tftp(
        zip_image_path,
        tftp_folder,
        eqs,
    )
    eq_sockets = get_v2l_sockets(
        mcu,
        eqs,
    )
    v2l_eyeqs = [
        V2LEyeQ(
            eq=eq,
            eq_socket=eq_sockets[eq.name],
            eq_component=eq_components[eq.name],
            tftp_folder=tftp_folder,
            log_file=open(
                socket_log_folder / f"{eq.name}.log",
                "w",
                buffering=1,
            ),
        )
        for eq in eqs
    ]
    with ThreadPoolExecutor(max_workers=len(eqs)) as ex:
        results = ex.map(lambda v2l_eyeq: v2l_eyeq.flash_eq(), v2l_eyeqs)
    assert all(result is None for result in results)
    mcu.reset_eq("all")
    logger.info("sleeping for 30 seconds and then checking board type and rev")
    time.sleep(30)
    with ThreadPoolExecutor(max_workers=len(eqs)) as ex:
        results = ex.map(
            functools.partial(
                validate_linux,
                board_name=board_name,
                board_rev=board_rev,
            ),
            eqs,
        )
    assert all(results)
    logger.info("Move from VOiS to Linux - success!")
