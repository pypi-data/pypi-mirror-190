from __future__ import annotations

import logging
import pathlib
import shlex
import subprocess
import time
from io import TextIOWrapper
from typing import Any


logger = logging.getLogger(__name__)


def set_logging(log_folder: pathlib.Path) -> None:
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGING_FMT = "[{asctime:}] | {levelname:^5s} | {name:^25s} : {message:s}"
    logging.basicConfig(
        format=LOGGING_FMT,
        level=logging.DEBUG,
        filename=log_folder / "main.log",
        filemode="w",
        style="{",
    )
    hdlr = logging.StreamHandler()
    fmt = logging.Formatter(fmt=LOGGING_FMT, style="{")
    hdlr.setFormatter(fmt)
    hdlr.setLevel(logging.INFO)
    logging.getLogger().addHandler(hdlr)


def power_cycle(
    sleep_between: float = 5,
    sleep_after: float = 10,
) -> None:
    logger.info("power off system: 'relay-off'")
    try:
        subprocess.run(
            ["relay-off"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as err:
        logger.error(f"power off - faild: {err}")
        raise
    logger.info(f"sleep {sleep_between} sec..")
    time.sleep(sleep_between)
    logger.info("power on system: 'relay-on'")
    try:
        subprocess.run(
            ["relay-on"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as err:
        logger.error(f"power on - faild: {err}")
        raise
    logger.info(f"sleep {sleep_after} sec..")
    time.sleep(sleep_after)


def run_on_linux(
    cmd: str,
    cmd_name: str,
    log_folder: pathlib.Path | None = None,
    timeout: float = 300,
    **kwargs: Any,
) -> subprocess.CompletedProcess[str]:
    stdout: TextIOWrapper | None
    stderr: TextIOWrapper | None
    if log_folder:
        cmd_log_folder = log_folder / cmd_name
        cmd_log_folder.mkdir(parents=True, exist_ok=True)
        stdout_file = cmd_log_folder / "stdout.log"
        stderr_file = cmd_log_folder / "stderr.log"
        stdout = stdout_file.open("w", buffering=1)
        stderr = stderr_file.open("w", buffering=1)
    else:
        stdout = stderr = None
    logger.info(f"[Linux] running cmd ({cmd_name}): {cmd!r}")
    return subprocess.run(
        shlex.split(cmd),
        bufsize=1,
        stdout=stdout,
        stderr=stderr,
        text=True,
        timeout=timeout,
        **kwargs,
    )
