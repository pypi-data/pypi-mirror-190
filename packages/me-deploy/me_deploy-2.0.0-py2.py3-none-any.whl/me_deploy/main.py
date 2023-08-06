from __future__ import annotations

import argparse
import logging
import pathlib

from me_setups.boards.gas52 import BoardType
from me_setups.boards.gas52 import Gas52Board
from me_setups.components.eqs import EyeQ5
from me_setups.components.mcu import Mcu
from me_setups.components.mcu import McuType

from me_deploy.mcu_tools import deploy_meaves_to_adam
from me_deploy.mcu_tools import deploy_meaves_to_asr
from me_deploy.mcu_tools import memtool_mcu_flash
from me_deploy.parser import add_parser_arguments
from me_deploy.parser import Args
from me_deploy.switch.upload import switch_upload
from me_deploy.tools import set_logging
from me_deploy.uboot import uboot_loader
from me_deploy.vois import vois_flasher
from me_deploy.vois_to_linux import v2l

logger = logging.getLogger("DEPLOY")


def deploy_board_to_uboot(
    eqs: list[EyeQ5],
    mcu: Mcu,
    log_folder: pathlib.Path,
    files_folder: pathlib.Path | None = None,
) -> None:
    assert files_folder
    eqs_set = set(eqs)
    eqs_on_uboot = uboot_loader.load_uboot(
        eqs,
        mcu,
        log_folder,
        files_folder,
    )
    assert eqs_on_uboot == eqs_set


def deploy_uboot_to_vois(
    eqs: list[EyeQ5],
    mcu: Mcu,
    log_folder: pathlib.Path,
    tftp_folder: pathlib.Path | None = None,
    files_folder: pathlib.Path | None = None,
) -> None:
    assert tftp_folder and files_folder
    eqs_set = set(eqs)
    eqs_on_uboot = vois_flasher.flash_eqs(
        eqs,
        mcu,
        log_folder,
        tftp_folder,
        files_folder,
    )
    assert set(eqs_on_uboot) == eqs_set


def full_flow(
    board: Gas52Board,
    log_folder: pathlib.Path,
    meaves_type: str | None = None,
    tftp_folder: pathlib.Path | None = None,
    uboot_files_folder: pathlib.Path | None = None,
    vois_files_folder: pathlib.Path | None = None,
    zip_image_path: pathlib.Path | None = None,
    board_name: str | None = None,
    board_rev: str | None = None,
    mcu_image_file: pathlib.Path | None = None,
    mcu_bl_file: pathlib.Path | None = None,
    skip_switch: bool | None = None,
    switch_ver: str | None = None,
) -> None:
    deploy_eol(
        board,
        log_folder,
        meaves_type,
        tftp_folder,
        uboot_files_folder,
        vois_files_folder,
        skip_switch,
    )

    deploy_eol_to_base(
        board,
        log_folder / "VOiS-to-Linux",
        tftp_folder,
        zip_image_path,
        board_name,
        board_rev,
    )

    end_of_flow(
        board,
        log_folder,
        mcu_image_file,
        mcu_bl_file,
        switch_ver,
    )


def end_of_flow(
    board: Gas52Board,
    log_folder: pathlib.Path,
    mcu_image_file: pathlib.Path | None = None,
    mcu_bl_file: pathlib.Path | None = None,
    switch_ver: str | None = None,
) -> None:
    if board.mcu.mcu_type == McuType.MEAVES_SINGLE_IMG:
        deploy_meaves_to_asr(board)
        board.board_type = BoardType.EVO
        board.mcu.mcu_type == McuType.ASR
    if board.mcu.mcu_type == McuType.MEAVES:
        assert mcu_image_file and mcu_bl_file
        deploy_meaves_to_adam(
            board,
            log_folder,
            mcu_image_file,
            mcu_bl_file,
            run_power_cycle=(switch_ver is None),
        )
        board.mcu.mcu_type == McuType.ADAM

    if switch_ver is not None:
        switch_upload(switch_ver, log_folder)


def deploy_eol(
    board: Gas52Board,
    log_folder: pathlib.Path,
    meaves_type: str | None = None,
    tftp: pathlib.Path | None = None,
    uboot_files: pathlib.Path | None = None,
    vois_files: pathlib.Path | None = None,
    skip_switch: bool | None = None,
) -> None:
    if not skip_switch:
        switch_upload("factory_image", log_folder, skip_power_cycle=True)

    assert meaves_type
    memtool_mcu_flash(
        board.mcu,
        log_folder,
        McuType[meaves_type],
    )

    deploy_board_to_uboot(
        board.eqs,
        board.mcu,
        log_folder / "UBOOT",
        uboot_files,
    )

    deploy_uboot_to_vois(
        board.eqs,
        board.mcu,
        log_folder / "VOiS",
        tftp,
        vois_files,
    )


def vois_to_linux(
    board: Gas52Board,
    log_folder: pathlib.Path,
    tftp_folder: pathlib.Path | None,
    zip_image_path: pathlib.Path | None,
    board_name: str | None,
    board_rev: str | None,
) -> None:
    assert tftp_folder and zip_image_path and board_name and board_rev
    v2l.flash(
        board.eqs,
        board.mcu,
        log_folder,
        tftp_folder,
        zip_image_path,
        board_name,
        board_rev,
    )


def deploy_eol_to_base(
    board: Gas52Board,
    log_folder: pathlib.Path,
    tftp_folder: pathlib.Path | None = None,
    zip_image_path: pathlib.Path | None = None,
    board_name: str | None = None,
    board_rev: str | None = None,
    mcu_image_file: pathlib.Path | None = None,
    mcu_bl_file: pathlib.Path | None = None,
    switch_ver: str | None = None,
) -> None:
    vois_to_linux(
        board,
        log_folder,
        tftp_folder,
        zip_image_path,
        board_name,
        board_rev,
    )

    end_of_flow(
        board,
        log_folder,
        mcu_image_file,
        mcu_bl_file,
        switch_ver,
    )


def main() -> int:
    parser = argparse.ArgumentParser(prog="Deploy")
    add_parser_arguments(parser)
    args = Args(**vars(parser.parse_args()))

    set_logging(args.log_folder)

    board = Gas52Board(board_type=BoardType[args.board_type])

    if args.cmd == "full":
        full_flow(
            board,
            args.log_folder,
            args.meaves_type,
            args.tftp,
            args.uboot_files,
            args.vois_files,
            args.zip_image,
            args.board_name,
            args.board_rev,
            args.mcu_image,
            args.mcu_bl,
            args.skip_switch,
            args.switch_ver,
        )

    elif args.cmd == "eol":
        deploy_eol(
            board,
            args.log_folder,
            args.meaves_type,
            args.tftp,
            args.uboot_files,
            args.vois_files,
            args.skip_switch,
        )

    elif args.cmd == "eol-to-base":
        deploy_eol_to_base(
            board,
            args.log_folder,
            args.tftp,
            args.zip_image,
            args.board_name,
            args.board_rev,
            args.mcu_image,
            args.mcu_bl,
            args.switch_ver,
        )

    elif args.cmd == "mcu-meaves":
        memtool_mcu_flash(
            board.mcu,
            args.log_folder,
            McuType[args.meaves_type],
        )

    elif args.cmd == "uboot":
        deploy_board_to_uboot(
            board.eqs,
            board.mcu,
            args.log_folder,
            args.uboot_files,
        )

    elif args.cmd == "vois":
        deploy_uboot_to_vois(
            board.eqs,
            board.mcu,
            args.log_folder,
            args.tftp,
            args.vois_files,
        )

    elif args.cmd == "switch":
        assert args.switch_ver
        switch_upload(
            args.switch_ver,
            args.log_folder,
        )

    elif args.cmd == "vois-to-linux":
        vois_to_linux(
            board,
            args.log_folder,
            args.tftp,
            args.zip_image,
            args.board_name,
            args.board_rev,
        )

    elif args.cmd == "meaves-to-asr":
        assert args.board_name and args.board_rev
        deploy_meaves_to_asr(board)

    elif args.cmd == "meaves-to-adam":
        deploy_meaves_to_adam(
            board,
            args.log_folder,
            args.mcu_image,
            args.mcu_bl,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
