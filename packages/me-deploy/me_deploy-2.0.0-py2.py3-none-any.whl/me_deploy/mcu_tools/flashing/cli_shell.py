#! /usr/bin/env python3

#
# INTEL CONFIDENTIAL
#
# Copyright (c) 2021 Intel Corporation All Rights Reserved.
#
# The source code contained or described herein and all documents related to
# the source code (Material) are owned by Intel Corporation or its suppliers
# or licensors. Title to the Material remains with Intel Corporation or its
# suppliers and licensors. The Material contains trade secrets and proprietary
# and confidential information of Intel or its suppliers and licensors. The
# Material is protected by worldwide copyright and trade secret laws and
# treaty provisions. No part of the Material may be used, copied, reproduced,
# modified, published, uploaded, posted, transmitted, distributed, or
# disclosed in any way without Intel's prior express written permission.
#
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise. Any license under such intellectual property rights must be
# express and approved by Intel in writing.
#

import argparse
import select
import time
import sys
import os

from utils.mcu_xmodem import xmodem_set_pipe, xmodem_send_file
from utils.mcu_comms import McuComms, CommsType
from utils.mcu_netflash import NetFlash, start_netflash_bin, start_netflash_hex, start_netflash_mcu, show_remaining_threads

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def dump_hex(byteseq):
    for i, byte in enumerate(byteseq):
        print("byte[%d]: 0x%x -- '%c'\n" % (i, ord(byte), byte))


class Shell:
    def __init__(self, com, show_thread, one_shot_command=False, skip_progress=False, test_abort=False):
        self.comms = com
        self.stdin = self.comms.get_stdin()
        self.remote = self.comms.get_remote()
        self.remote_socket = self.comms.get_remote_socket()
        self.callbacks = {}
        self.remote_read_size = self.comms.get_read_size()
        self.one_shot_command = one_shot_command
        self.pre_command = None
        self.show_thread = show_thread
        self.skip_progress = skip_progress

    def flush_remote(self, print_remote=False):
        while True:
            r, _, _ = select.select([self.remote_socket], [], [], 0.1)
            if self.remote_socket in r:
                if print_remote:
                    feedback = self.remote.read(self.remote_read_size)
                    sys.stdout.write(feedback.decode("utf-8", "strict"))
                    sys.stdout.flush()
                else:
                    self.remote.read(self.remote_read_size)
            else:
                # nothing else, timed out...
                return

    def add_command_local_callback(self, command, callback, *arguments):
        callbacks = self.callbacks.setdefault(command, [])
        callbacks.append([callback, arguments])

    def run_command_callbacks(self, command):
        command = command.strip()
        # found = False
        # for _command in self.callbacks.keys():
        #     print("checking %s vs %s" % (command, _command))
        for _command in self.callbacks:
            if command.startswith(_command) and command.find('?') == -1 and command.find('status') == -1:
                # found = True
                callbacks = self.callbacks[_command]
                for callback_args in callbacks:
                    [callback, arguments] = callback_args
                    return callback(*arguments)
        return None
        # if not found:
        #     print("Callback for %s not found!!" % command)

    # pylint: disable=too-many-branches
    def main_loop(self):
        self.flush_remote()
        if self.one_shot_command is not None:
            # Run the command and leave
            self.remote.write("\n".encode())
            time.sleep(0.4)
            self.flush_remote()
            self.one_shot_command += "\n"
            self.pre_command = "\n\n"
            self.remote.write(self.pre_command.encode())
            # give the MCU some time to process and free the ethernet buffers for the pre_command
            time.sleep(0.4)
            self.remote.write(self.one_shot_command.encode())
            time.sleep(0.4)
            result = self.run_command_callbacks(self.one_shot_command)
            # show flashing and xmodem results:
            if result:
                if isinstance(result, NetFlash):
                    # XMODEM result is already boolean
                    result.show_flashing_result(result.get_flashing_result())  # This prints to the screen
                    result = result.get_flashing_result()
            self.flush_remote(True)
            show_remaining_threads(self.show_thread)
            print("\nGoodbye...\n")
            if os.name == 'posix':
                if result:
                    sys.exit(EXIT_SUCCESS)
                else:
                    sys.exit(EXIT_FAILURE)
            else:
                # Apperently there is a bug in windows with using exit(), the threads aren't closing:
                os.kill(os.getpid(), 9)
                # For more info on the bug check commit Ibe9f8bb18f1c86fcb84938b61fa6871f2a35513b
        command = ''
        while True:
            try:
                r, _, _ = select.select([self.stdin, self.remote_socket], [], [], 0.5)
                if self.remote_socket in r:
                    feedback = self.remote.read(self.remote_read_size)
                    if feedback:
                        sys.stdout.write(feedback.decode("utf-8", "strict"))
                        sys.stdout.flush()
                if self.stdin in r:
                    if os.name == 'posix':
                        command += self.stdin.readline()
                    else:
                        command += self.stdin.readline().decode()
                    if command.endswith('\n') or command.endswith('\r\n'):
                        self.remote.write(command.encode())
                        self.run_command_callbacks(command)
                        command = ''
            except KeyboardInterrupt:
                print("\nCtrl+C received, exiting Shell ...\n")
                break


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description=__doc__)
    group = argparser.add_mutually_exclusive_group(required=True)
    optional = argparser.add_argument_group('optional arguments')
    group.add_argument(
        '-U', '--udp-socket',
        metavar='<ip:port>',
        default=None,
        help='Socket address in the form <ip:port>')
    group.add_argument(
        '-P', '--pseudo-tty',
        metavar='<tty dev>',
        default=None,
        help='Pseudo tty file in the form /dev/pts/xxx')
    group.add_argument(
        '-S', '--serial',
        metavar='<tty dev@baudrate>',
        default=None,
        help='Serial port to use and baudrate in the form /dev/ttyUSB0@115200')
    argparser.add_argument(
        '-f', '--file',
        metavar='<file>',
        default=None,
        help='Firmware hex file to be flashed or json file to be added to filesystem')
    argparser.add_argument(
        '-c', '--command',
        default=None,
        help='Run the command and exit')
    argparser.add_argument(
        '-t', '--timeout',
        metavar=None,
        default=7.0,
        type=float,
        help='timeout in seconds (default is 7s)')
    optional.add_argument(
        '--show_thread',
        metavar=None,
        default=False,
        type=bool,
        help='show remaining threads after program execution, i.e., true or false')
    optional.add_argument(
        '--skip_progress',
        action='store_true',
        help='Skip progress bar log to console')
    optional.add_argument(
        '--test_abort',
        action='store_true',
        help='Abort the transfer before completion, for target testing, only works for netflash_mcu and netflash_img')
    args = argparser.parse_args()
    host = None

    if args.timeout is not None:
        timeout = args.timeout
    if args.udp_socket is not None:
        host, port = args.udp_socket.split(':')
        comms = McuComms(CommsType.udp, args.show_thread, udp_host=host, udp_port=int(port))
    elif args.pseudo_tty is not None:
        comms = McuComms(CommsType.pseudo_tty, args.show_thread, pseudo_tty=args.pseudo_tty)
    elif args.serial is not None:
        serial_port, serial_baudrate = args.serial.split('@')
        comms = McuComms(CommsType.serial, args.show_thread, serial_port=serial_port, serial_baudrate=serial_baudrate)
    shell = Shell(comms, args.show_thread, args.command)
    if args.serial is not None:
        # If we are using serial we need to turn the echo off:
        if args.command is None:
            shell.remote.write('test program init\n'.encode())
            shell.remote.flush()
    if args.file is not None:
        readsize = comms.get_read_size()
        xmodem_set_pipe(comms.get_remote())
        shell.add_command_local_callback("test xmodem t", xmodem_send_file, args.file, readsize)
        shell.add_command_local_callback("test xmodem x", xmodem_send_file, args.file, readsize)
        shell.add_command_local_callback("test xmodem f", xmodem_send_file, args.file, readsize)
        shell.add_command_local_callback("test xmodem a", xmodem_send_file, args.file, readsize)
        shell.add_command_local_callback("test fs -t", xmodem_send_file, args.file, readsize)
        shell.add_command_local_callback("test skm_http r", xmodem_send_file, args.file, readsize)
        shell.add_command_local_callback("RunTest otp blob", xmodem_send_file, args.file, readsize)
        if host is not None:
            shell.add_command_local_callback("netflash_bin", start_netflash_bin, host, comms, args.file, args.show_thread, None, timeout, args.skip_progress)
            shell.add_command_local_callback("netflash_hex", start_netflash_hex, host, comms, args.file, args.show_thread, None, timeout, args.skip_progress)
            shell.add_command_local_callback("netflash_mcu", start_netflash_mcu, host, comms, args.file, args.show_thread, None, timeout, args.skip_progress,
                                             args.test_abort)
            shell.add_command_local_callback("netflash_img", start_netflash_mcu, host, comms, args.file, args.show_thread, None, timeout, args.skip_progress,
                                             args.test_abort)
    shell.main_loop()
    comms.close_stdin()

    # Turning the echo back on:
    if args.serial is not None:
        shell.remote.write('test program exit\n'.encode())
        shell.remote.flush()

    show_remaining_threads(args.show_thread)
    print("Bye!!!")
    # ultimate kill...
    os.kill(os.getpid(), 9)
