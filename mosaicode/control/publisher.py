# -*- coding: utf-8 -*-
"""
This module create the web server.
"""
import SimpleHTTPServer
import SocketServer
import threading
import os
import socket
import fcntl
import struct
from mosaicode.system import System as System

class Publisher():
    """
    This class contains methods related to running web server.
    """
    # ----------------------------------------------------------------------
    def __init__(self):
        self.httpd = None
        self.ip = None
        self.port = 8080
        self.httpd_thread = None

    # ----------------------------------------------------------------------
    def is_running(self):
        return self.httpd is not None

    # ----------------------------------------------------------------------
    def stop(self):
        if self.httpd is not None:
            self.__stop_server()

    # ----------------------------------------------------------------------
    def start(self):
        if self.httpd is None:
            self.__start_server()

    # ----------------------------------------------------------------------
    def get_ip(self, count):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        try:
            IP = s.getsockname()[count]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP


    # ----------------------------------------------------------------------
    def __start_server(self):
        while self.httpd is None:
            try:
                path = '/tmp/'
                my_path = os.curdir
                os.chdir(path)
                count = 0
                System.log("Trying to run the server on ips and ports:")
                while count < 3:
                    self.ip = self.get_ip(count)
                    System.log(str(self.ip) + ":" + str(self.port))
                    count = count + 1

                handler = SimpleHTTPServer.SimpleHTTPRequestHandler
                SocketServer.ThreadingTCPServer.allow_reuse_address = True
                self.httpd = SocketServer.ThreadingTCPServer(('', self.port), handler)
                self.httpd_thread = threading.Thread(target=self.httpd.serve_forever)
                self.httpd_thread.setDaemon(True)
                self.httpd_thread.start()
                count = 0
                System.log("Server running on ip and port:")
                while count < 3:
                    self.ip = self.get_ip(count)
                    System.log(str(self.ip) + ":" + str(self.port))
                    count = count + 1

                os.chdir(my_path)
            except:
                self.port = self.port + 1

    # ----------------------------------------------------------------------
    def __stop_server(self):
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd.socket.close()
            self.httpd_thread.join()
            self.httpd = None
            System.log("Server stopped")