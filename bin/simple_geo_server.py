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
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

from lib.LogClient import LogClient
from heater.Heater import Interval

log = LogClient("simple_geo_server")


class S(BaseHTTPRequestHandler):
    heater_interval = Interval(log)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        log.info('url path: ' + self.path)
        if self.path == '/favicon.ico':
            return

        if self.path == '/heater':
            heater_set = S.heater_interval.heater_set()
            next_moment = S.heater_interval.check_when()

            if not heater_set:
                log.info("heater not set, next moment to check: %s" % next_moment)
                self.wfile.write(bytes("no|%s,0" % next_moment, 'UTF-8'))

            if next_moment < 30000:
                duration = S.heater_interval.heat_duration()
                log.info("heater time! time off: %s, duration: %s" % (next_moment, duration))
                self.wfile.write(bytes("yes|0,%s" % duration, 'UTF-8'))
            else:
                log.info("heater set, but not yet time to heat. time left: %s" % next_moment)
                self.wfile.write(bytes("no|%s,0" % next_moment, 'UTF-8'))

            log.info('heater: request')
        else:
            url_split = urllib.parse.urlsplit(self.path)
            args = urllib.parse.parse_qs(url_split.query)
            log.info("geo: %s" % args)
            print(args)
            self.wfile.write(bytes("<html><body><h1>hi!</h1></body></html>", 'UTF-8'))

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_headers()
        print("POST: " + post_data)
        self.wfile.write("<html><body><h1>POST!</h1><pre>" + post_data + "</pre></body></html>")


def run(server_class=HTTPServer, handler_class=S, port=8060):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

