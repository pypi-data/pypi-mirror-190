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

import logging
import time
import sys
import os

from xmodem import XMODEM

logging.basicConfig(level=logging.INFO)

xmodem_pipe = None


def getc(size, timeout=1):
    assert xmodem_pipe
    # print("getc waiting for %d bytes to %s" % (size, xmodem_pipe))
    return xmodem_pipe.read(size)


def putc(data):
    assert xmodem_pipe
    # print("putc %d bytes to %s" % (len(data), xmodem_pipe))
    xmodem_pipe.write(data)
    return len(data)


def xmodem_set_pipe(pipe):
    # pylint: disable=global-statement
    global xmodem_pipe
    xmodem_pipe = pipe


def xmodem_send_file(file_name, read_size, start_timeout=10.0):
    print("Waiting for starting character (up to %d seconds)..." % start_timeout)
    start_time = time.time()
    c0 = ""
    # give a chance to the MCU to print some info before starting the transfer
    while True:
        c = xmodem_pipe.read(read_size).decode("utf-8", "strict")
        if (c0 + c).find("CC") != -1:
            # got the start character
            break
        if time.time() - start_time > start_timeout:
            print("Timeout waiting for the transfer, cancelled!")
            return False
        sys.stdout.write(c)
        sys.stdout.flush()
        if c != '':
            c0 = c
    print("Sending %s..." % (file_name))
    xmodem = XMODEM(getc, putc)
    stream = open(file_name, 'rb')
    start_time = time.time()
    is_success = xmodem.send(stream)
    dt = time.time() - start_time
    stat_info = os.stat(file_name)
    print("%d bytes sent in %0.3f seconds -- %d bytes/seconds" % (stat_info.st_size, dt, stat_info.st_size / dt))
    return is_success
