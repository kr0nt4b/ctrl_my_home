#!/usr/bin/env python
"""
Intended target: OSMC device
"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
from Speaker.SwitchSpeaker import SwitchSpeaker
from Logging.LogClient import LogClient
from HarmonyChecker import HarmonyChecker
from Kodi.Kodi import kodi_stop, kodi_start, radio_play
import threading

log = LogClient("simple_cmd_server")


class HttpHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        if self.path.startswith('/ab/current_activity'):
            self.wfile.write(checker.get_last_activity() + "\n")

        if self.path.startswith('/reboot'):
            os.system('reboot')

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

        if self.path == '/kodi/stop':
            log.info("kodi stop")
            kodi_stop()

        if self.path == '/kodi/start':
            log.info("kodi start")
            kodi_start()

        if self.path == '/radio/on':
            radio_play()

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


def run(server_class=HTTPServer, handler_class=HttpHandler, port=9999):
    server_address = ('', port)

    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    log.info("Starting simple_cmd_server")
    try:
        httpd.serve_forever()
    except:
        pass


def callback(activity):
    print('Switched activity. New:' + activity)
    if activity != 'Music':
        speaker = SwitchSpeaker(log)
        speaker.internal()
    else:
        speaker = SwitchSpeaker(log)
        speaker.external()


if __name__ == "__main__":
    handler = HttpHandler
    checker = HarmonyChecker(log, callback)
    thread = threading.Thread(target=checker.start)
    thread.start()

    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]), handler_class=handler)
    else:
        run()

    checker.stop()

#######################
# if self.path == '/tv/on':
#     cmd = 'echo "on 0" | cec-client RPI -s -d 4'
#     os.system(cmd)
#     log.info("cmd: tv on")
#
# if self.path == '/tv/off':
#     cmd = 'echo "standby 0" | cec-client -s -m -d 1'
#     os.system(cmd)
#     log.info("cmd: tv off")
# if self.path == '/tv/hdmi3':
#     cmd = 'echo "tx 4F:82:30:00" | cec-client -d 1 -s'
#     os.system(cmd)
#     log.info("hdmi3")
#
# if self.path == '/tv/kodi':
#     cmd = 'echo "tx 4F:82:20:00" | cec-client -d 1 -s'
#     os.system(cmd)
#     log.info("switch to kodi (HDMI 2)")
#
# if self.path == '/tv/hdmi1':
#     cmd = 'echo "tx 4F:82:10:00" | cec-client -d 1 -s'
#     os.system(cmd)
#     log.info("hdmi1")
