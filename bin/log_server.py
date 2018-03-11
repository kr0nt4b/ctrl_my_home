#!/usr/bin/python2
"""
    Simple socket server using threads
"""

import socket
import sys
from thread import *
import os
import logging

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 9998  # Arbitrary non-privileged port

LOG_FORMAT = '%(asctime)-15s %(message)s'
SMART_LOG = '/var/log/smart/smarthome.log'


class LogServer:

    @staticmethod
    def init_logging():
        smart_log_path = os.path.dirname(SMART_LOG)
        if not os.path.exists(os.path.dirname(smart_log_path)):
            os.mkdir(smart_log_path)
        logging.basicConfig(filename=SMART_LOG, level=logging.DEBUG, format=LOG_FORMAT)
        return logging.getLogger('log_server')

    def __init__(self):
        self.logger = self.init_logging()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.info('Socket created')

        # Bind socket to local host and port
        try:
            self.sock.bind((HOST, PORT))
        except socket.error as msg:
            self.logger.info('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        self.logger.info('Socket bind complete')

        # Start listening on socket
        self.sock.listen(10)
        self.logger.info('Socket now listening')

    # Function for handling connections. This will be used to create threads
    def client_thread(self, connection):
        # Sending message to connected client
        connection.send('connected\n')  # send only takes string

        # infinite loop so that function do not terminate and thread do not end.
        while True:

            # Receiving from client
            data = connection.recv(1024)
            reply = 'OK\n'
            if not data:
                break

            self.logger.info(data)
            connection.sendall(reply)

        # came out of loop
        connection.close()

    def start(self):
        # now keep talking with the client
        while True:
            # wait to accept a connection - blocking call
            conn, addr = self.sock.accept()
            self.logger.info('Connected with ' + addr[0] + ':' + str(addr[1]))

            # start new thread takes 1st argument as a function name to be run, second
            # is the tuple of arguments to the function.
            start_new_thread(self.client_thread, (conn,))

        self.sock.close()


if __name__ == "__main__":
    log_server = LogServer()
    try:
        log_server.start()
    except KeyboardInterrupt as e:
        print(e.message)
