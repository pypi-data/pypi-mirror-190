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

from enum import Enum
import socket
import errno
try:
    from serial import Serial as serial
except ImportError:
    try:
        from serial import serial
    except ImportError:
        import serial
import sys
import os
from utils.win_filesocket import WinFileSocketListener


STDIN_WIN_HOST = "localhost"
STDIN_WIN_PORT_MIN = 9998
STDIN_WIN_NB_PORTS = 10

CAN_MSG_LEGACY = 8
CAN_MSG_SIZE_FD = 64


class CommsType(Enum):
    serial = 1
    udp = 2
    pseudo_tty = 3


class UdpSocket:
    def __init__(self, udp_ip, udp_port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_addr = (udp_ip, udp_port)
        print("Using UDP on %s" % repr(self.client_addr))

    def read(self, nbytes=1024):
        try:
            data, _ = self.socket.recvfrom(nbytes)
            return data
        except Exception as e:
            print("UdpSocket read exception (nbytes = %d): %s" % (nbytes, str(e)))
            raise e

    def readline(self):
        try:

            byte_size = 1024
            data, _ = self.socket.recvfrom(byte_size)
            return data
        except Exception as e:
            print("UdpSocket readline exception: %s" % str(e))
            raise e

    def write(self, data):
        try:
            # print("Sending %s to %s" % (data, self.client_addr))
            return self.socket.sendto(data, self.client_addr)
        except Exception as e:
            print("UdpSocket write exception: %s" % str(e))
            raise e

    def flush(self):
        pass


class TcpSocket:
    def __init__(self, tcp_ip, tcp_port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client_addr = (tcp_ip, tcp_port)
            print("Using TCP on %s" % repr(self.client_addr))
        except KeyboardInterrupt:
            print("CTRL+C received, exiting %s init..." % (self.__class__.__name__))
            self.socket.close()
            os._exit(0)

    def connect(self, addr=None):
        if addr is not None:
            self.client_addr = addr
        print("TcpSocket connecting %s" % str(self.client_addr))
        return self.socket.connect(self.client_addr)

    def reconnect(self):
        try:
            self.socket.close()
            while True:
                try:
                    print("Connection lost, retrying...")
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.socket.settimeout(1.0)
                    self.socket.connect(self.client_addr)
                    self.socket.settimeout(None)
                    break
                except socket.timeout:
                    print("Connection timeout...")
                    self.socket.close()
            self.socket.send(b"\n\n")
        except KeyboardInterrupt:
            print("CTRL+C received, exiting %s reconnect..." % (self.__class__.__name__))
            sys.exit(0)

    def read(self, nbytes):
        try:
            data = self.socket.recv(nbytes)
            return data
        except socket.error as se:
            print(se.errno, errno.ECONNRESET)
            if se.errno == errno.ECONNRESET:
                self.reconnect()
                print("TcpSocket reconnected")
                return self.read(nbytes)
        except Exception as e:
            print("TcpSocket read exception: %s" % str(e))
            raise e

    def readline(self):
        try:
            byte_size = 1024
            data = self.socket.recv(byte_size)
            return data
        except socket.error as se:
            if se.errno == errno.ECONNRESET:
                self.reconnect()
                return self.readline()
        except Exception as e:
            print("TcpSocket readline exception: %s" % str(e))
            raise e

    def write(self, data):
        try:
            # print("Sending %s to %s" % (data, self.client_addr))
            return self.socket.send(data)
        except socket.error as se:
            if se.errno == errno.ECONNRESET:
                self.reconnect()
                return self.socket.send(data)
        except Exception as e:
            print("TcpSocket write exception: %s" % str(e))
            raise e

    def flush(self):
        pass

    def fileno(self):
        return self.socket.fileno()


class McuComms:
    def __init__(self, comms_type, flag, pseudo_tty=None, serial_port=None,
                 serial_baudrate=None, udp_host=None, udp_port=None):
        # pylint: disable=too-many-arguments

        self.comms_type = comms_type
        self.flag = flag
        self.std_listener = None
        self.remote_listener = None
        assert self.comms_type in CommsType
        if self.comms_type == CommsType.serial:
            assert serial_port is not None and serial_baudrate is not None
            self.serial_port = serial_port
            self.serial_baudrate = serial_baudrate
            self.remote = serial(serial_port, serial_baudrate, timeout=0.4,
                                 bytesize=8, parity='N', stopbits=1, xonxoff=False,
                                 rtscts=False, dsrdtr=False)
            if os.name != "posix":
                (self.remote_listener, self.remote) = \
                        self.open_file_socket_listener("Serial", self.flag, self.remote, self.get_read_size())
        elif self.comms_type == CommsType.pseudo_tty:
            assert pseudo_tty is not None
            self.pseudo_tty = pseudo_tty
            self.remote = open(pseudo_tty, "wb+", buffering=0)
            self.remote.flush()
        elif self.comms_type == CommsType.udp:
            assert udp_host is not None and udp_port is not None
            self.udp_host = udp_host
            self.udp_port = udp_port
            self.remote = UdpSocket(udp_host, udp_port)
        print("Connection establishment")
        self.remote.write(b"\n\n")

    def get_remote(self):
        return self.remote

    def get_remote_socket(self):
        if self.comms_type == CommsType.udp:
            res = self.remote.socket
        else:
            res = self.remote
        return res

    def get_read_size(self):
        if (self.comms_type == CommsType.serial or
                self.comms_type == CommsType.pseudo_tty):
            res = 1
        else:
            res = 1024
        return res

    def close_stdin(self):
        try:
            if self.std_listener:
                self.std_listener.socket.close()
                self.std_listener.close()
        except socket.error:
            pass
        try:
            if self.remote_listener:
                self.remote_listener.close()
        except socket.error:
            pass

    def get_stdin(self):
        if os.name != "posix":
            # windows can't use stdin in select
            (self.std_listener, stdin) = self.open_file_socket_listener("StdInOut", self.flag)
            return stdin
        return sys.stdin

    def open_file_socket_listener(self, name, flag, inoutfile=None, readsize=1):
        self.flag = flag
        min_port = STDIN_WIN_PORT_MIN
        max_port = min_port + STDIN_WIN_NB_PORTS
        for port in range(min_port, max_port):
            try:
                print("McuComms: Trying WinFileSocketListener(%s) port %d..." % (name, port))
                listener = WinFileSocketListener(STDIN_WIN_HOST, port, name, self.flag, inoutfile, readsize)
                listener.start()
                socket_ = TcpSocket(STDIN_WIN_HOST, port)
                socket_.connect((STDIN_WIN_HOST, port))
                print("McuComms: Connected to WinFileSocketListener(%s) port %d" % (name, port))
                return (listener, socket_)
            except socket.error as se:
                print("\n================================================================\n")
                print("[ERROR]: Could not connect to WinFileSocketListener('{0}'); Exception: '{1}'".format(name, str(se)))
                print("\n================================================================\n")
        # not connected
        print("\n================================================================\n")
        print("[FATAL]: Max sockets reached for file to socket emulation...")
        print("Please kill some of the clients or change STDIN_WIN_NB_PORTS")
        print("\n================================================================\n")
        sys.exit(-1)

# if __name__ == "__main__":
#    m = McuComms(CommsType.serial, self.flag, serial_port="/dev/ttyUSB0", serial_baudrate=115200)
