from __future__ import annotations

import argparse
import pathlib
from dataclasses import dataclass

from me_setups.boards.gas52 import BoardType
from me_setups.components.mcu import McuType

from me_deploy.constants import RESOURCES_DIR
from me_deploy.switch.upload import supported_ver


def add_parser_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--log-folder",
        metavar="<path>",
        type=pathlib.Path,
        default=pathlib.Path("logs"),
        help="path to log folder, if not exits, create one.",
    )
    board_types = [e.name for e in BoardType]
    parser.add_argument(
        "--board-type",
        metavar="<type>",
        type=str,
        choices=board_types,
        required=True,
        help=f"Type of board choose from: {'/'.join(board_types)}",
    )
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    full_arguments(
        subparsers.add_parser(
            "full",
            help="Full flow -- board -> EOL -> Base",
        ),
    )

    eol_arguments(
        subparsers.add_parser(
            "eol",
            help="move the board from any state to EOL state",
        ),
    )

    eol_to_base_arguments(
        subparsers.add_parser(
            "eol-to-base",
            help="move the board from EOL state to BASE",
        ),
    )

    meaves_arguments(
        subparsers.add_parser(
            "mcu-meaves",
            help="deploy MEAVES using memtool",
        ),
    )

    uboot_arguments(
        subparsers.add_parser(
            "uboot",
            help="move board to U-boot",
        ),
    )

    vois_arguments(
        subparsers.add_parser(
            "vois",
            help="move the board from U-boot to VOiS",
        ),
    )

    switch_arguments(
        subparsers.add_parser(
            "switch",
            help="flash switch version",
        ),
    )

    vois_to_linux_arguments(
        subparsers.add_parser(
            "vois-to-linux",
            help="move the board from VOiS to Linux",
        ),
    )

    subparsers.add_parser(
        "meaves-to-asr",
        help="move MCU from MEAVES single image to ASR",
    )

    meaves_to_adam_arguments(
        subparsers.add_parser(
            "meaves-to-adam",
            help="move the MCU from MEAVES to ADAM using NETFLASH",
        ),
    )


def tftp_arguments(parser: argparse.ArgumentParser) -> None:
    try:
        parser.add_argument(
            "--tftp",
            metavar="<path>",
            type=pathlib.Path,
            help="path to tftp folder",
        )
    except argparse.ArgumentError:
        pass


def meaves_arguments(parser: argparse.ArgumentParser) -> None:
    mcu_types = ["MEAVES", "MEAVES_SINGLE_IMG"]
    parser.add_argument(
        "--meaves-type",
        metavar="<type>",
        type=str,
        choices=mcu_types,
        default=McuType.MEAVES.name,
        help=f"type of MCU choose from: {'/'.join(mcu_types)}",
    )


def uboot_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--uboot-files",
        metavar="<path>",
        type=pathlib.Path,
        help="path to U-boot files folder",
        default=RESOURCES_DIR / "uboot",
    )


def vois_arguments(parser: argparse.ArgumentParser) -> None:
    tftp_arguments(parser)
    parser.add_argument(
        "--vois-files",
        metavar="<path>",
        type=pathlib.Path,
        help="path to VOiS files folder",
        default=RESOURCES_DIR / "vois",
    )


def eol_arguments(parser: argparse.ArgumentParser) -> None:
    meaves_arguments(parser)
    uboot_arguments(parser)
    vois_arguments(parser)
    parser.add_argument(
        "--skip-switch",
        action="store_true",
        help="skip flashing blank file for the switch",
    )


def switch_arguments(parser: argparse.ArgumentParser) -> None:
    switch_versions = supported_ver.keys()
    parser.add_argument(
        "--switch-ver",
        type=str,
        metavar="<ver>",
        choices=switch_versions,
        help=f"the version to flash choose from: {'/'.join(switch_versions)}",
        default=None,
    )


def vois_to_linux_arguments(parser: argparse.ArgumentParser) -> None:
    tftp_arguments(parser)
    parser.add_argument(
        "--zip-image",
        metavar="<path>",
        type=pathlib.Path,
        help="path to Linux zip file",
    )
    parser.add_argument(
        "--board-name",
        metavar="<name>",
        type=str,
        default="GAS52-B4",
        help="name of the board to check at the end of V2L",
    )
    parser.add_argument(
        "--board-rev",
        metavar="<rev>",
        type=str,
        default="0x3",
        help="rev of the board to check at the end of V2L",
    )


def meaves_to_adam_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--mcu-image",
        metavar="<path>",
        type=pathlib.Path,
        default=None,
        help="path to ADAM image file",
    )
    parser.add_argument(
        "--mcu-bl",
        metavar="<path>",
        type=str,
        default=None,
        help="path to ADAM bootloader file",
    )


def eol_to_base_arguments(parser: argparse.ArgumentParser) -> None:
    vois_to_linux_arguments(parser)
    meaves_to_adam_arguments(parser)
    switch_arguments(parser)


def full_arguments(parser: argparse.ArgumentParser) -> None:
    eol_arguments(parser)
    eol_to_base_arguments(parser)


@dataclass
class Args:
    cmd: str
    log_folder: pathlib.Path
    board_type: str | None = None
    meaves_type: str | None = None
    uboot_files: pathlib.Path | None = None
    tftp: pathlib.Path | None = None
    vois_files: pathlib.Path | None = None
    zip_image: pathlib.Path | None = None
    skip_switch: bool | None = None
    board_name: str | None = None
    board_rev: str | None = None
    mcu_image: pathlib.Path | None = None
    mcu_bl: pathlib.Path | None = None
    switch_ver: str | None = None
