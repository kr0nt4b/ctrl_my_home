#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2013 Tristan Fischer (sphere@dersphere.de)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import xbmcaddon
import xbmcgui
import xbmc
import os
import time
import sys

import urllib2
import socket


def get_current_activity_name(client):
    activity = client.get_current_activity()
    config = client.get_config()
    for i in config['activity']:
        if int(i['id']) == activity:
            return i['label']
    return ""


addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_path = addon.getAddonInfo('path')


CONTROL_MOVING_BACKGROUND = 1
CONTROL_ANIMATED_RAINBOW = 2


class Screensaver(xbmcgui.WindowXMLDialog):

    class ExitMonitor(xbmc.Monitor):

        def __init__(self, exit_callback):
            self.exit_callback = exit_callback

        def onScreensaverDeactivated(self):
            self.exit_callback()

    def onInit(self):
        try:
            sock = urllib2.urlopen("http://localhost:9999/ab/current_activity", timeout=1)
            current_activity = sock.read()
            sock.close()
            if 'Video' in current_activity:
                self.log('Into standby')
                os.system('echo "standby 0" | /usr/osmc/bin/cec-client -s -m -d 1')
            else:
                self.log('Skipping standby. Current activity is: %s' % current_activity)
        except socket.timeout as e:
            self.log('Connection problem with harmony hub: %s' % e)
        except Exception as e:
            self.log('General problem with harmony hub: %s' % e)

        self.exit_monitor = self.ExitMonitor(self.exit)
        self.handle_settings()

    def handle_settings(self):
        if addon.getSetting('moving_background') == 'true':
            self.getControl(CONTROL_MOVING_BACKGROUND).setVisible(False)
        if not addon.getSetting('animated_rainbow') == 'true':
            self.getControl(CONTROL_ANIMATED_RAINBOW).setVisible(False)

    def exit(self):
        self.abort_requested = True
        self.exit_monitor = None
        try:
            sock = urllib2.urlopen("http://localhost:9999/ab/current_activity", timeout=1)
            current_activity = sock.read()
            sock.close()
            if 'Video' in current_activity:
                self.log('Out standby')
                os.system('echo "on 0" | /usr/osmc/bin/cec-client RPI -s -d 4')
                time.sleep(2)
                os.system('echo "tx 4F:82:20:00" | cec-client -d 1 -s')
            else:
                self.log('Stay in standby. Current activity is: %s' % current_activity)
        except socket.timeout as e:
            self.log('Connection problem with harmony hub: %s' % e)
        except Exception as e:
            self.log('General problem with harmony hub: %s' % e)
        self.close()

    def log(self, msg):
        xbmc.log(u'Nyan Cat Screensaver: %s' % msg)


if __name__ == '__main__':
    screensaver = Screensaver(
        'script-%s-main.xml' % addon_name,
        addon_path,
        'default',
    )
    screensaver.doModal()
    del screensaver
    sys.modules.clear()
