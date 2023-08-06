from __future__ import annotations

import logging
import select
import socket
import threading
import time
from enum import Enum


EQS_MCU_NAMES = {
    "EQ5_PBCM_0000": "EQ1.0",
    "EQ5_PBCM_0001": "EQ1.1",
    "EQ5_PBCM_0010": "EQ2.0",
    "EQ5_PBCM_0011": "EQ2.1",
    "all": "all",
    "ALL": "all",
}


class McuType(Enum):
    MEAVES = "meaves"
    ADAM = "adam"
    MEAVES_ASR = "asr"


logger = logging.getLogger(__name__)


MCU_ADDRESS = {
    McuType.MEAVES: ("192.168.19.20", 9995),
    McuType.ADAM: ("192.168.19.16", 4200),
    McuType.MEAVES_ASR: ("192.168.19.16", 9995),
}


class Mcu:
    def __init__(
        self,
        mcu_type: McuType = McuType.MEAVES,
    ):
        self.mcu_type = mcu_type
        self.address = MCU_ADDRESS[mcu_type]

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(5.0)

        self.lock = threading.Lock()

    def run_cmd(self, cmd: str) -> bytes:
        logger.debug(f"running cmd = {cmd!r}")
        cmd = f"{cmd}\n"
        cmd_b = cmd.encode()
        with self.lock:
            assert self.socket.sendto(cmd_b, self.address) == len(cmd_b)
            time.sleep(0.1)
            response = self.get_response()
        return response

    def get_response(self) -> bytes:
        result = b""
        while True:
            r, _, _ = select.select([self.socket], [], [], 0.1)
            if self.socket in r:
                feedback = self.socket.recv(1024)
                result += feedback
                time.sleep(0.01)
            else:
                break
        return result

    def get_eq_name(self, eq_name: str) -> str:
        return EQS_MCU_NAMES[eq_name]

    def set_eq_bootmode(self, eq_name: str | None, mode: str) -> bool:
        if eq_name is None:
            eq_mcu_name = "all"
        else:
            eq_mcu_name = self.get_eq_name(eq_name)
        if self.mcu_type == McuType.ADAM:
            cmd = f"set -e {eq_mcu_name} -b {mode}"
        elif self.mcu_type in (McuType.MEAVES, McuType.MEAVES_ASR):
            cmd = f"set {eq_mcu_name} bootmode {mode}"
        else:
            raise NotImplementedError
        self.run_cmd(cmd)
        return True

    def set_eq_uboot(self, eq_name: str | None, status: str) -> bool:
        if eq_name is None:
            eq_mcu_name = "all"
        else:
            eq_mcu_name = self.get_eq_name(eq_name)
        if self.mcu_type == McuType.ADAM:
            cmd = f"set -e {eq_mcu_name} -u {status}\n"
        elif self.mcu_type in (McuType.MEAVES, McuType.MEAVES_ASR):
            cmd = f"set {eq_mcu_name} uboot {status}\n"
        else:
            raise NotImplementedError
        self.run_cmd(cmd)
        return True

    def reset_eq(self, eq_name: str | None = None) -> bool:
        if eq_name is None:
            eq_mcu_name = "all"
        else:
            eq_mcu_name = self.get_eq_name(eq_name)
        if self.mcu_type == McuType.ADAM:
            cmd = f"reset -e {eq_mcu_name}"
        elif self.mcu_type in (McuType.MEAVES, McuType.MEAVES_ASR):
            cmd = f"reset {eq_mcu_name}"
        else:
            raise NotImplementedError
        self.run_cmd(cmd)
        return True
