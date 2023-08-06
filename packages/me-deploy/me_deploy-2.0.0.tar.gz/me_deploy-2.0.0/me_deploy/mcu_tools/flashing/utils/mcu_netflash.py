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

import select
import struct
import time
import sys
import re
import os
import logging
import threading

from threading import Thread, Event
from utils.mcu_comms import UdpSocket
from utils.mcu_hex_tools import hex_prepare_chunks

CONTROL_CODE_ACK = chr(0x3)
CONTROL_CODE_EOT = chr(0x4)
CONTROL_CODE_ABORT = chr(0x5)

logger = logging.getLogger("CLI_Regression")


class NetFlash(Thread):
    def __init__(self, protocol, host, port, show_threads_flag, log_file=None, chunks=None, bin_file=None, transfer_size=256, skip_progress=False,
                 test_abort=False):
        # pylint: disable=too-many-arguments
        super(NetFlash, self).__init__(name="NetFlash")
        self.port = port
        self.stop_event = Event()
        self.transfer_size = transfer_size
        self.chunks = chunks
        self.bin_file = bin_file
        self.protocol = protocol
        self.rx_bytes = 0
        self.tx_bytes = 0
        self.target = host
        self.tx_size = 0
        self.log_file = log_file
        self.flashing_result = False
        self.show_threads_flag = show_threads_flag
        self.outfile_handle = None
        self.erase_time = 0
        self.program_time = 0
        self.skip_progress_display = skip_progress
        self.test_abort = test_abort
        try:
            if self.log_file is not None:
                self.outfile_handle = open(log_file, 'a')
        except OSError as e:
            print("\n================================================================\n")
            print("[ERROR]: Logger file '{0}' could not be opened; Exception: '{1}'".format(self.log_file, str(e)))
            print("\n================================================================\n")

    def stop(self):
        self.stop_event.set()

    def open_socket(self):
        if self.protocol == "UDP":
            socket = UdpSocket(self.target, self.port)
        return socket

    def log(self, *args):
        if self.log_file is not None:
            self.outfile_handle.write(*args)
        logger.info(*args)

    def show_stats(self, et, dt):
        self.erase_time = int(et * 1000.0)
        self.program_time = int(dt * 1000.0)
        self.log("================================================================\n")
        self.log("================================================================\n")
        self.log("===== NetFlash stats (client side):                        =====\n")
        self.log("===== erase time:   % 8d ms                            =====\n" % self.erase_time)
        self.log("===== program time: % 8d ms                            =====\n" % self.program_time)
        self.log("===== rx bytes:     % 8d bytes                         =====\n" % self.rx_bytes)
        self.log("===== tx bytes:     % 8d bytes                         =====\n" % self.tx_bytes)
        self.log("===== rx bandwidth: % 8d bytes/seconds                 =====\n" % int(self.rx_bytes / dt))
        self.log("===== tx bandwidth: % 8d bytes/seconds                 =====\n" % int(self.tx_bytes / dt))
        self.log("================================================================\n")
        self.log("================================================================\n")

    def set_flashing_result(self, result):
        if result == CONTROL_CODE_ACK:
            self.flashing_result = True
        else:
            self.flashing_result = False

    def get_flashing_result(self):
        return self.flashing_result

    def show_flashing_result(self, result):
        if result is True:
            self.log("================== flashing result: success ==================\n\n")
        else:
            self.log("================== flashing result: error ==================\n\n")

    # print iterations progress
    # see https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    def print_progress_bar(self, prefix='', suffix='', decimals=1, length=100, fill='*'):
        # pylint: disable=too-many-arguments
        """
        Call in a loop to create terminal progress bar
        @params:
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        progress = self.tx_bytes
        total = self.tx_size
        percent = ("{0:." + str(decimals) + "f}").format(100 * (progress / float(total)))
        filled_length = int(length * progress // total)
        progress_bar = fill * filled_length + '-' * (length - filled_length)
        sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, progress_bar, percent, suffix))
        sys.stdout.flush()
        # print New Line on Complete
        if progress >= total:
            print()

    def prepare_start_message(self, socket):
        if self.bin_file is not None:
            file_size_32 = os.stat(self.bin_file).st_size
        else:
            file_size_32 = len(self.chunks)
        crc32 = 0xDEADBEEF
        message = struct.Struct('<II').pack(file_size_32, crc32)
        self.tx_size = file_size_32
        self.log("\nFile size 0x%08x(%d), crc32 0x%08x\n" % (file_size_32, file_size_32, crc32))
        written = socket.write(message)
        if written != len(message):
            self.log("================================================================\n")
            self.log("[ERROR]: Wrote %d bytes on %d posted!\n" % (written, len(message)))
            self.log("================================================================\n")
            return False
        self.tx_bytes += written

        ack = socket.read(1).decode("utf-8", "strict")
        self.rx_bytes += 1
        if ack == CONTROL_CODE_ACK:
            # print("########## Target sent ACK...")
            return True
        if ack == CONTROL_CODE_EOT:
            # print("########## Target sent EOT...")
            return False
        if ack == CONTROL_CODE_ABORT:
            print("########## ERROR: target aborted the transfer!")
            return False
        return False

    def dump_bytes(self, bytes_):
        self.log("\nDumping %d bytes" % (len(bytes_)))
        for index in range(0, len(bytes_), 8):
            if index + 7 >= len(bytes_):
                return
            b0 = bytes_[index]
            b1 = bytes_[index + 1]
            b2 = bytes_[index + 2]
            b3 = bytes_[index + 3]
            b4 = bytes_[index + 4]
            b5 = bytes_[index + 5]
            b6 = bytes_[index + 6]
            b7 = bytes_[index + 7]
            self.log(" %02x %02x %02x %02x %02x %02x %02x %02x" % (int(b0), int(b1), int(b2), int(b3), int(b4), int(b5), int(b6), int(b7)))

    def run(self):
        # pylint: disable=too-many-branches, too-many-statements
        self.log("%s running..." % (self.__class__.__name__))
        start_time = time.time()
        socket = self.open_socket()
        if not self.prepare_start_message(socket):
            socket.write(CONTROL_CODE_EOT.encode())
            return
        # enters the main loop
        erase_time = time.time() - start_time
        start_time = time.time()
        if self.bin_file is not None:
            f = open(self.bin_file, "rb")
        else:
            chunks_index = 0
        while not self.stop_event.is_set():
            if self.bin_file is not None:
                message = f.read(self.transfer_size)
                if len(message) == 0:
                    break
            else:
                if chunks_index + self.transfer_size < len(self.chunks):
                    message = self.chunks[chunks_index:chunks_index + self.transfer_size]
                    chunks_index += self.transfer_size
                    if(self.test_abort and (chunks_index + self.transfer_size > len(self.chunks)/2)):
                        return
                elif chunks_index == len(self.chunks):
                    break
                else:
                    message = self.chunks[chunks_index:len(self.chunks)]
                    chunks_index = len(self.chunks)
            # print("Sending  a chunk of %d bytes -- 0x%02x%02x%02x%02x -- 0x%02x%02x%02x%02x" % (len(message), int(message[3]),
            #  int(message[2]), int(message[1]), int(message[0]), int(message[-1]), int(message[-2]), int(message[-3]), int(message[-4]) ) )
            # print("Sending %d bytes: %s -- %s" % (len(message), [hex(c) for c in message[0:4]], [hex(c) for c in message[-4:]]))
            # print("Sending %d bytes: %s" % (len(message), [hex(c) for c in message]))
            # self.dump_bytes(message)
            written = socket.write(message)
            if written != len(message):
                self.log("================================================================\n")
                self.log("[CLI_TOOL_ERROR]: Wrong number of bytes sent!")
                self.log("[CLI_TOOL_ERROR]: Sent %d bytes, expected to send %d bytes\n" % (written, len(message)))
                self.log("================================================================\n")
                socket.write(CONTROL_CODE_ABORT.encode())
                return
            # print("########## Sent %d bytes, waiting for control code..." % written)
            self.tx_bytes += written
            if not self.skip_progress_display:
                self.print_progress_bar()
            ack = socket.read(1).decode("utf-8", "strict")
            self.rx_bytes += 1
            if ack == CONTROL_CODE_ACK:
                # print("########## Target sent ACK...")
                self.set_flashing_result(ack)
                continue
            if ack == CONTROL_CODE_EOT:
                # print("########## Target sent EOT...")
                self.set_flashing_result(ack)
                return
            if ack == CONTROL_CODE_ABORT:
                self.set_flashing_result(ack)
                self.log("================================================================\n")
                self.log("[CLI_TOOL_ERROR]: Target aborted the transfer!")
                self.log("================================================================\n")
                return
            self.log("CLI_TOOL_WARNING: Target sent unknown ack 0x%x" % ord(ack))
        # send the termination character to the target
        socket.write(CONTROL_CODE_EOT.encode())
        self.tx_bytes += 1
        # show the stats
        self.show_stats(erase_time, time.time() - start_time)
        # show currently running threads
        show_remaining_threads(self.show_threads_flag)
        # close remaning sockets
        socket.socket.close()
        if self.bin_file:
            f.close()
        return


def wait_for_transfer_start(remote, start_timeout):
    logger.info("Waiting for the target to start the flashing (up to %d seconds)...", start_timeout)
    start_time = time.time()
    udp_pattern = re.compile(r'UDP binary transfer going-on \(port ([0-9]+), page_size ([0-9]+), flash_start 0x([0-9a-fA-F]+), transfer_size ([0-9]+)\).*')
    while True:
        r, _, _ = select.select([remote.socket], [], [], 0.1)
        if time.time() - start_time > start_timeout:
            logger.info("Timeout waiting for the target to start the transfer, cancelled!")
            return None
        if remote.socket not in r:
            continue
        c = remote.read(1024).decode("utf-8", "strict")
        msg_begin_pos = c.find('UDP binary transfer going-on')
        msg_end_pos = c.find(').') + 2
        if (msg_begin_pos != -1 and msg_end_pos != -1):
            m = udp_pattern.match(c[msg_begin_pos:msg_end_pos])
            if m is None:
                logger.info("Found the start message for UDP but couldn't decode it in '%s'!", c[msg_begin_pos:msg_end_pos])
                return None
            (port, page_size, flash_start, transfer_size) = m.groups()
            return ("UDP", int(port), int(page_size), int(flash_start, 16), int(transfer_size))
        if len(c) > 0:
            logger.info(c)


def start_netflash_bin(host, comms, bin_file, show_threads, log_file=None, timeout=1.0, skip_progress=False):
    # pylint: disable=too-many-arguments
    remote = comms.get_remote()
    result = wait_for_transfer_start(remote, timeout)
    if result is None:
        return None
    (protocol, port, _, _, transfer_size) = result
    logger.info("Starting the transfer thread using '%s'!", str(result))
    try:
        task = NetFlash(protocol, host, port, show_threads, log_file, bin_file=bin_file, transfer_size=transfer_size, skip_progress=skip_progress)
        task.setDaemon(True)
        task.start()
        task.join()
        return task
    except KeyboardInterrupt:
        logger.info("CTRL+C received, Netlfash exiting...\n")
        show_remaining_threads(show_threads)
        task.stop()
        task.join()
        raise KeyboardInterrupt


def start_netflash_hex(host, comms, hex_file, show_threads, log_file=None, timeout=1.0, skip_progress=False):
    # pylint: disable=too-many-arguments
    remote = comms.get_remote()
    result = wait_for_transfer_start(remote, timeout)
    if result is None:
        return None
    (protocol, port, page_size, chunk_root_address, transfer_size) = result
    logger.info("Starting the transfer thread using '%s'!", str(result))
    try:
        chunks = hex_prepare_chunks(hex_file, page_size, chunk_root_address)
        task = NetFlash(protocol, host, port, show_threads, log_file, chunks=chunks, transfer_size=transfer_size, skip_progress=skip_progress)
        task.setDaemon(True)
        task.start()
        task.join()
        return task
    except AssertionError as ae:
        logger.error("AssertionError during hex flashing: %s", str(ae))
        raise ae
    except KeyboardInterrupt:
        logger.info("CTRL+C received, Netflash exiting...\n")
        show_remaining_threads(show_threads)
        task.stop()
        task.join()
        raise KeyboardInterrupt


def start_netflash_mcu(host, comms, hex_file, show_threads, log_file=None, timeout=1.0, skip_progress=False, test_abort=False):
    # pylint: disable=too-many-arguments
    remote = comms.get_remote()
    result = wait_for_transfer_start(remote, timeout)
    if result is None:
        return None
    (protocol, port, page_size, chunk_root_address, transfer_size) = result
    print("result = " + str(result))
    logger.info("Starting the transfer thread using '%s'!", str(result))
    try:
        magic_bytes = struct.pack('<I', 0xFEEDDEAD)
        chunks = magic_bytes + hex_prepare_chunks(hex_file, page_size, chunk_root_address + len(magic_bytes))
        task = NetFlash(protocol, host, port, show_threads, log_file, chunks=chunks, transfer_size=transfer_size, skip_progress=skip_progress,
                        test_abort=test_abort)
        task.setDaemon(True)
        task.start()
        task.join()
        return task
    except AssertionError as ae:
        logger.error("AssertionError during mcu flashing: %s", str(ae))
        raise ae
    except KeyboardInterrupt:
        logger.info("CTRL+C received, Netflash exiting...\n")
        show_remaining_threads(show_threads)
        task.stop()
        task.join()
        raise KeyboardInterrupt


def show_remaining_threads(show_threads):
    if show_threads is True:
        count = threading.active_count()
        max_count = 0
        while max_count < count:
            max_count = count
        print("\nNumber of active threads: " + str(count) + " \n")
        for thread in threading.enumerate():
            print("" + thread.name + " \n")
    else:
        return None
