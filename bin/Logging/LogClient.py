#!/usr/bin/python2

import socket
import sys
import logging


class LogClient:

    def __init__(self, name):
        self.name = name
        self.name = name
        self.host = socket.gethostname()
        self.port = 9998
        self.buffer_size = 2000
        self.connected = False
        self.tcpClient = None

        self.connect()

        if not self.connected:
            root = logging.getLogger('')
            root.setLevel(logging.DEBUG)
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            root.addHandler(handler)

    def connect(self):
        self.tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print >> sys.stdout, 'connecting to %s:%s' % (self.host, self.port)

        try:
            self.tcpClient.connect((self.host, self.port))
            self.connected = True
            print >> sys.stdout, 'connected'
        except socket.error as e:
            print(e.strerror)
            self.connected = False


    def debug(self, message):
        return self.send("%s DEBUG: %s", message)
        
    def info(self, message):
        return self.send("%s INFO: %s", message)

    def send(self, format, message):
        if not self.connected:
            return logging.debug(message)
        print >>sys.stdout, 'sending "%s"' % message
        try:
            self.tcpClient.send(format % (self.name, message))
        except socket.error as e:
            self.tcpClient.close()

        while True:
            data = self.tcpClient.recv(self.buffer_size)
            if data.endswith("\n"):
                data = data.strip()
                print >>sys.stdout, 'received "%s"' % data
                return data == "OK"

    def close(self):
        print >>sys.stdout, 'closing socket'
        self.tcpClient.close()


if __name__ == "__main__":
    log = LogClient("TEST")
    log.info("Hoi, daar")
    log.info("Hoi, daar1")
    log.info("Hoi, daar2")

