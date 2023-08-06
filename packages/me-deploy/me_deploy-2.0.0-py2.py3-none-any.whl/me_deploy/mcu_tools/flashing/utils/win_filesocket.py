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

from threading import Thread, Event
import socket
import time
import sys
import os


class FileInListener(Thread):
    def __init__(self, listener, name, show_thread, infile, readsize):
        # pylint: disable=too-many-arguments
        super(FileInListener, self).__init__(name="FileInListener")
        self.name = "%s(%s)" % (self.__class__.__name__, name)
        self.show_thread = show_thread
        self.stop_event = Event()
        self.stopped = False
        self.listener = listener
        self.readsize = readsize
        self.infile = infile if infile is not None else sys.stdin
        self.socket = None

    def run(self):
        file_in_listener_socket_timeout = 0.01
        print("%s running" % self.name)
        self.socket, addr = self.listener.socket.accept()
        self.socket.settimeout(file_in_listener_socket_timeout)
        print("%s connected to %s" % (self.name, str(addr)))
        self.listener.set_connection(self.socket)
        print("%s set the listener connection..." % self.name)
        while not self.stop_event.is_set():
            try:
                data = self.infile.read(self.readsize)
                if isinstance(data, bytes):
                    data = data.decode()
                if not self.stop_event.is_set():
                    self.socket.send(data.encode())
            except KeyboardInterrupt:
                print("Ctrl+C received, exiting FileInListener...")
                self.stopped = True
                break
            except socket.error:
                pass
            except UnicodeDecodeError:
                pass
        print("%s leaving " % self.name)
        self.stopped = True


class FileOutListener(Thread):
    def __init__(self, name, show_thread, outfile):
        super(FileOutListener, self).__init__(name="FileOutListener")
        self.name = "%s(%s)" % (self.__class__.__name__, name)
        self.show_thread = show_thread
        self.connected = Event()
        self.stop_event = Event()
        self.stopped = False
        self.outfile = outfile if outfile is not None else sys.stdout
        self.socket = None

    def set_connection(self, client_conn):
        self.socket = client_conn
        self.connected.set()

    def run(self):
        file_out_listener_socket_timeout = 0.2
        try:
            while not self.connected.is_set():
                time.sleep(0.5)
            self.socket.settimeout(file_out_listener_socket_timeout)
            print("%s Connected" % self.name)
            while not self.stop_event.is_set():
                try:
                    # print("listening on the socket...")
                    data = self.socket.recv(1024)
                    if not data:
                        print('data None...')
                    else:
                        if self.name == "FileOutListener(Serial)" or os.path.isfile(self.outfile):
                            self.outfile.write(data)
                except socket.timeout:
                    pass
        except KeyboardInterrupt:
            print("CTRL C received, exiting FileOutListener...")
            pass
        print("%s leaving" % self.name)
        self.stopped = True


class WinFileSocketListener:
    def __init__(self, host, port, name="WinSocket", show_thread=None, inoutfile=None, readsize=1, timeout=5.0):
        # pylint: disable=too-many-arguments
        assert(host is not None and port is not None)
        self.name = "%s(%s)" % (self.__class__.__name__, name)
        self.show_thread = show_thread
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(1)
        self.socket.settimeout(timeout)
        self.in_listener = FileInListener(self, name, show_thread, inoutfile, readsize)
        self.out_listener = FileOutListener(name, show_thread, inoutfile)
        self.inoutfile = inoutfile
        time.sleep(0.2)

    def start(self):
        self.in_listener.start()
        self.out_listener.start()

    def stop(self):
        self.in_listener.stop_event.set()
        self.out_listener.stop_event.set()

    def set_connection(self, client_conn):
        self.out_listener.set_connection(client_conn)

    def close(self):
        if not self.in_listener.stop_event.is_set():
            self.in_listener.stop_event.set()
            self.out_listener.stop_event.set()
        print("Waiting...")
        time.sleep(2)
        self.in_listener.join(0.5)
        self.out_listener.join(0.5)
        self.in_listener.socket.shutdown(socket.SHUT_RDWR)
        self.in_listener.socket.close()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        if self.inoutfile:
            self.inoutfile.close()


if __name__ == "__main__":
    sleep_time = 5
    sl = WinFileSocketListener("localhost", 9998)
    thread_timeout = 0.5
    sl.start()
    print("Waiting 5 seconds")
    time.sleep(sleep_time)
    print("Stopping...")
    sl.stop()
    print("Stopped and waiting 5 more seconds")
    time.sleep(sleep_time)
    print("WinFileSocketListener.in_listener.stopped: ", sl.in_listener.stopped)
    print("WinFileSocketListener.out_listener.stopped: ", sl.out_listener.stopped)
    sl.out_listener.join(thread_timeout)
    sl.in_listener.join(thread_timeout)
    print("WinFileSocketListener.in_listener.stopped: ", sl.in_listener.stopped)
    print("WinFileSocketListener.out_listener.stopped: ", sl.out_listener.stopped)
    sl.close()
    print("Leaving...")
    sys.exit(0)
