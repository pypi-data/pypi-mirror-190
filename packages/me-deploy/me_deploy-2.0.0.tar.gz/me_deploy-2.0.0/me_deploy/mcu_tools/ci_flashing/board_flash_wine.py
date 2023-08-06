#!/usr/bin/env python3

# INTEL CONFIDENTIAL

# Copyright 2022 Intel Corporation All Rights Reserved.

# The source code contained or described herein and all documents related to
# the source code ("Material") are owned by Intel Corporation or its suppliers
# or licensors. Title to the Material remains with Intel Corporation or its
# suppliers and licensors. The Material contains trade secrets and proprietary
# and confidential information of Intel or its suppliers and licensors. The
# Material is protected by worldwide copyright and trade secret laws and
# treaty provisions. No part of the Material may be used, copied, reproduced,
# modified, published, uploaded, posted, transmitted, distributed, or
# disclosed in any way without Intel's prior express written permission.

# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise. Any license under such intellectual property rights must be
# express and approved by Intel in writing.

# Unless otherwise agreed by Intel in writing, you may not remove or alter this
# notice or any other notice embedded in Materials by Intel or Intel's
# suppliers or licensors in any way.

import sys
import os
import argparse
import logging
from subprocess import CalledProcessError, run, Popen, check_call, TimeoutExpired
import time
import json

# List of supported board types:
BOARD_TYPES = {'TC297': 'TriBoard_TC29xB_das.cfg',
               'TC397': 'appkit.cfg',
               'GAS': 'gas52.cfg',
               'EPM6': 'TriBoard_TC38xA_das.cfg',
               'EPM51': 'EPM51_EPM5_EPC5_TC38xA_das.cfg',
               'SB': 'GAS52_Sensorboard_TC39xB_das.cfg',
               'CECU': 'TriBoard_TC38xA_das.cfg',
               'vision1': 'TriBoard_TC38xA_das.cfg',
               'vision2': 'TriBoard_TC38xA_das.cfg',
               'vision3': 'TriBoard_TC38xA_das.cfg',
               'primary': 'epm58.cfg',
               'secondary': 'epm58.cfg'}

TOOL_DIR = os.path.dirname(os.path.dirname(__file__))
MEMTOOL_PATH = "/memtool/IMTMemtool.exe"
RESET_BOARD = "/memtool/board_reset.sh"
WORKSPACE = "z:" + os.path.abspath(os.getcwd())
TARGETS_WORKSPACE = "z:" + os.path.abspath(TOOL_DIR) + "/ci_flashing/memtool"
PNG_PATH = os.path.abspath(TOOL_DIR) + "/ci_flashing/PNG/"
DAS_HOME = os.environ['DAS_HOME']
DAS_SERVER = DAS_HOME + "/servers/udas/UDAS_Console_DAP_Telegrams &"
XVFB_FILE = "/tmp/.X99-lock"
XVFB = "Xvfb :99 &"


def generate_appkit_file(path, hex_files):
    with open(path, "w+") as f:
        f.write("connect\n")
        for hex in hex_files:
            f.write(f"open_file {hex}\n")
            f.write("select_all_sections\n")
            f.write("add_selected_sections\n")
        f.write("program\n")
        f.write("exit\n")
        f.write("disconnect\n")
        f.write("exit\n")


def reset_board(args):
    # rest the board before and after flashing
    if not os.path.exists(RESET_BOARD):
        print("board_reset.sh is not present in /memtool of this machine which is needed for reset of the board")
    else:
        os.system("/memtool/board_reset.sh")


def kill_das(args):
    logging.info("kill the existing DAS server")
    os.system("pkill DAS")


def toggle_ykush(args):
    if args.board_type in ["primary", "secondary", "vision1",  "vision2", "vision3"]:
        try:
            with open("/memtool/ykush.json", 'r') as ykushfile:
                ykush = json.load(ykushfile)
                ykushfile.close()
        except IOError:
            logging.critical(
                "Can't get ykush details. please create ykush details here /memtool/ykush.json")
            sys.exit(-1)

        YKUSH1 = ykush['YKUSH1']
        YKUSH2 = ykush['YKUSH2']
        YKUSHOFF = f"ykushcmd -s {YKUSH1} -d a && ykushcmd -s {YKUSH2} -d a"
        global YKUSHON
        YKUSHON = f"ykushcmd -s {YKUSH1} -u a && ykushcmd -s {YKUSH2} -u a"
        P = ykush['PRIMARY'][YKUSH1]
        S = ykush['SECONDARY'][YKUSH1]
        V1 = ykush['VISION1'][YKUSH2]
        V2 = ykush['VISION2'][YKUSH2]
        V3 = ykush['VISION3'][YKUSH2]

        if (args.board_type == "primary"):
            logging.info("Toggle YKUSH UART to connect only primary miniwiggler\n")
            check_call(f"{YKUSHOFF} && ykushcmd -s {YKUSH1}  -u {P}", shell=True)
        elif (args.board_type == "secondary"):
            logging.info("Toggle YKUSH UART to connect only Secondary miniwiggler\n")
            check_call(f"{YKUSHOFF}  && ykushcmd -s {YKUSH1}  -u {S}", shell=True)
        elif (args.board_type == "vision1"):
            logging.info("Toggle YKUSH UART to connect only vision1 miniwiggler\n")
            check_call(f"{YKUSHOFF}  && ykushcmd -s {YKUSH2}  -u {V1}", shell=True)
        elif (args.board_type == "vision2"):
            logging.info("Toggle YKUSH UART to connect only vision2 miniwiggler\n")
            check_call(f"{YKUSHOFF}  && ykushcmd -s {YKUSH2}  -u {V2}", shell=True)
        elif (args.board_type == "vision3"):
            logging.info("Toggle YKUSH UART to connect only vision3 miniwiggler\n")
            check_call(f"{YKUSHOFF}  && ykushcmd -s {YKUSH2}  -u {V3}", shell=True)


def erase_partition(args):
    import pyautogui
    # Debug folder
    DEBUG_DIR = "/memtool/DEBUG_ERASE_FLASH/" + args.buildid + "/"
    os.system("mkdir " + DEBUG_DIR)
    TIMEOUT = 60
    partitions = args.erase_partitions
    f = open("erase", "w+")
    f.write("connect\n")
    f.close()
    cmd = f"wine {MEMTOOL_PATH} {WORKSPACE}/erase -c {TARGETS_WORKSPACE}/{args.boardCFG}"
    logging.info("Calling cmd %s", cmd)
    Popen(cmd, shell=True)

    # Checking batch file execution
    batch_executed = pyautogui.locateOnScreen(PNG_PATH + 'batch_done.PNG')
    connected = pyautogui.locateOnScreen(PNG_PATH + 'connected.PNG')
    start_time = time.time()
    while not (batch_executed and connected):
        pyautogui.screenshot().save(DEBUG_DIR + "ERASE_connect_stage.png")
        batch_executed = pyautogui.locateOnScreen(PNG_PATH + 'batch_done.PNG')
        connected = pyautogui.locateOnScreen(PNG_PATH + 'connected.PNG')
        if (pyautogui.locateOnScreen(PNG_PATH + 'das_error.PNG')):
            raise ValueError('DAS server connection error !')
        if (time.time() - start_time > TIMEOUT):
            raise ValueError('Batch file was not executed properly, board is not connected to memtool !')
    pyautogui.click(PNG_PATH + 'ok_btn.PNG')

    # Deleting partitions
    for i in range(int(partitions)):
        time.sleep(1)
        pyautogui.screenshot().save(DEBUG_DIR + "ERASE_before_erasing_stage.png")
        pyautogui.click(PNG_PATH + 'erase.PNG')
        time.sleep(1)
        pyautogui.click(PNG_PATH + 'start.PNG')
        success = pyautogui.locateOnScreen(PNG_PATH + 'success.PNG')
        start_time = time.time()
        while not (success):
            pyautogui.screenshot().save(DEBUG_DIR + "ERASE_partition_" + str(i+1) + "_stage.png")
            success = pyautogui.locateOnScreen(PNG_PATH + 'success.PNG')
            if (pyautogui.locateOnScreen(PNG_PATH + 'failed.PNG')):
                raise ValueError('Flashing failed !!!')
            if (time.time() - start_time > TIMEOUT):
                raise ValueError('Erasing partition number' + str(i+1) + 'has timed out !')
        logging.info("Partition number " + str(i+1) + " erased succesfuly")
        pyautogui.click(PNG_PATH + 'exit.PNG')
        time.sleep(2)
        pyautogui.click(PNG_PATH + 'arrow.PNG')
        time.sleep(2)
        pyautogui.press('down')
        pyautogui.press('enter')

    # Moving back to the first partition

    pyautogui.screenshot().save(DEBUG_DIR + "ERASE_last_stage.png")
    pyautogui.click(PNG_PATH + 'arrow.PNG')
    time.sleep(1)
    for i in range(int(partitions) + 1):
        pyautogui.press('up')
    pyautogui.press('enter')
    pyautogui.click(PNG_PATH + 'exit.PNG')


def flash_board(args):
    IMAGE_PATH = [f"{WORKSPACE}/{img}" for img in args.image_names]

    # Generate appkit file
    generate_appkit_file("./appkit", IMAGE_PATH)
    logging.info("reseting  %s board  before flashing the board", args.board_type)
    reset_board(args)
    # run Das server before flashing
    Popen(DAS_SERVER, shell=True)

    # Erase partitions
    if (args.erase_partitions):
        try:
            erase_partition(args)
        except ValueError as err:
            logging.error(err)
            logging.error("Failed erasing partitions. Killing memtool")
            sys.exit(-1)

    count = 1
    while count <= 3:  # Many times flashing fails for network failure. Try 3 times.
        try:
            cmd = f"wine {MEMTOOL_PATH} {WORKSPACE}/appkit -c {TARGETS_WORKSPACE}/{args.boardCFG}"
            logging.info("Calling cmd %s (with timeout)", cmd)
            wine_process = run(cmd, shell=True, check=True, timeout=90, capture_output=True)
            error = wine_process.stderr
            if 'err:' in error.decode("utf-8"):
                raise CalledProcessError(returncode=1, cmd="", stderr="Flashing failed. Please check if $DISPLAY set to :99 and DAS server is running")
                print("\n ##### ERROR #####\n")
            break

        except (CalledProcessError, TimeoutExpired)as e:
            print("\n ##### ERROR #####\n")
            logging.error(e.stderr)
            print("\n ##### ERROR #####\n")
            logging.info("reseting  %s board and kill DAS server", args.board_type)
            os.system("pkill DAS")
            reset_board(args)
            if count == 3:
                if args.board_type in ["primary", "secondary", "vision1",  "vision2", "vision3"]:
                    logging.info("Toggle all ykush connections back to ON\n")
                    check_call(YKUSHON, shell=True)
                sys.exit(-1)
            count += 1

    logging.info("Flashig of " + " " + args.board_type + "  " + "MCU is finished sucessfully")
    logging.debug(wine_process.stdout)
    logging.info("reseting  %s board  after flashing the board and kill DAS server", args.board_type)
    kill_das('DAS')
    reset_board(args)


def main():
    # Get Arg configurations
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action='count',
                        default=0, help="increase output verbose")
    parser.add_argument("-i", "--image", action='append',
                        help="path to the image that needs to be flashed", required=True)
    parser.add_argument("-b", "--board_type",
                        choices=BOARD_TYPES.keys(), required=True)
    parser.add_argument("-j", "--buildid", default='Default',
                        help="Jenkins Build ID")
    parser.add_argument("-ep", "--erase_partitions", type=int, choices=range(1, 6),
                        help="Number of partitions to erase")
    args = parser.parse_args()

    LOGGING_FORMAT = '%(levelname)s: %(message)s'

    # Check if the image is given
    if args.verbose > 0:
        logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT)
    else:
        logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)

    args.image_names = []
    for image in args.image:
        if not os.path.isfile(image):
            logging.critical("Invalid image file: %s", image)
            sys.exit(-1)
        elif not image.endswith('.hex'):
            logging.critical("Unsupported image: %s. Please use .hex file.", image)
            sys.exit(-1)
        else:
            args.image_names.append(os.path.relpath(image))

    args.boardCFG = BOARD_TYPES[args.board_type]

    # Check if XVFB and DAS server is running
    kill_das('DAS')
    if not os.path.exists(XVFB_FILE):
        print("Xvfb is not set properly and DAS server is not started")
        Popen(XVFB, shell=True)
        Popen(DAS_SERVER, shell=True)

    toggle_ykush(args)
    flash_board(args)
    if args.board_type in ["primary", "secondary", "vision1",  "vision2", "vision3"]:
        logging.info("Toggle all ykush connections back to ON\n")
        check_call(YKUSHON, shell=True)
    logging.info("Sleeping for 10s to allow the %s board to come to CLI SHELL after flashing", args.board_type)
    time.sleep(10)
    logging.info("SUCCESS")


if __name__ == "__main__":
    main()
