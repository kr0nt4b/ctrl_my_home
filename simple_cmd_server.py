#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
from Speaker.SwitchSpeaker import SwitchSpeaker
from Logging.LogClient import LogClient

log = LogClient("simple_cmd_server")


class S(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        if self.path.startswith('/amp/'):
            button = self.path[5:]
            if button in ('KEY_POWER_ON', 'KEY_POWER_OFF', 'KEY_AUX'):
                sub = 'Marantz_RC2000x'
            else:
                sub = 'Marantz'
            cmd = 'irsend -d /var/run/lirc/lircd-lirc0 SEND_ONCE %s %s' % (sub, button)
            os.system(cmd)
            self.wfile.write("OK\n")
            log.info("cmd: %s" % cmd)
            
            if button == 'KEY_RECORDER2':
                speaker = SwitchSpeaker(log)
                speaker.external()

            if button in ('KEY_POWER', 'KEY_POWER_TOGGLE','KEY_TUNER', 'KEY_AUX', 'KEY_CD', 'KEY_RECORDER1', 'KEY_PHONO'):
                speaker = SwitchSpeaker(log)
                speaker.internal()

        if self.path.startswith('/dvd/'):
            button = self.path[5:]
            remote = 'dvd'
            cmd = 'irsend -d /var/run/lirc/lircd-lirc0 SEND_ONCE %s %s' % (remote, button)
            os.system(cmd)
            self.wfile.write("OK\n")
            log.info("cmd: %s" % cmd)

        if self.path.startswith('/light/'):
            code = self.path[7:]
            cmd = '/usr/bin/codesend %s' % code
            os.system(cmd)
            self.wfile.write("OK\n")
            log.info("cmd: %s" % cmd)

        if self.path == '/speaker/internal':
            speaker = SwitchSpeaker(log)
            speaker.internal()
            self.wfile.write("OK\n")
            log.info("cmd: internal speaker")

        if self.path == '/speaker/external':
            speaker = SwitchSpeaker(log)
            speaker.external()
            self.wfile.write("OK\n")
            log.info("cmd: external speaker")

        if self.path == '/tv/on':
            cmd = 'echo "tx 20:04" | cec-client RPI -s -d 4'
            os.system(cmd)
            log.info("cmd: tv on")

        if self.path == '/tv/off':
            cmd = 'echo "tx 20:36" | cec-client RPI -s -d 4'
            os.system(cmd)
            log.info("cmd: tv off")

        if self.path == '/tv/kodi':
            cmd = 'echo "tx 2F:82:20:00" | cec-client RPI -s -d 4'
            os.system(cmd)
            log.info("tv to kodi")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST not implemented</h1></body></html>")


def run(server_class=HTTPServer, handler_class=S, port=9999):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    log.info("Starting simple_cmd_server")
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
