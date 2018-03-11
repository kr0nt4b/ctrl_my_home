#!/usr/bin/python

import socket
import sys
import os
import time
from Logging.LogClient import LogClient
from Speaker.SwitchSpeaker import SwitchSpeaker
from Domoticz.Domoticz import DomoticzClient

log = LogClient("lirc_sockread")
log.info("Starting lirc_sockread")

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
lirc_unix_sock = '/var/run/lirc/lircd-lirc0'
log.info('connecting to %s' % lirc_unix_sock)

UNDEFINED = 255
MAIN_LIGHT = 5
DINING_LIGHT = 24
DESK_LIGHT = 38
CORNER_LIGHT = 32
KITCHEN_LIGHT = 4
BOX_LIGHT = 40
CHRISTMAS_LIGHTS = 51
WINDOW_LIGHT = 39

try:
    sock.connect(lirc_unix_sock)
except socket.error, msg:
    log.info(msg)
    sys.exit(1)

log.info('connected to %s' % lirc_unix_sock)
modifier = UNDEFINED

domoticz = DomoticzClient(log)

while True:
    data = sock.recv(160)

    if len(data) == 0:
        time.sleep(5)
        continue

    log.debug("raw: %s (length: %s)" % (data, len(data)))
    tokens = data.split(' ')
    remote = tokens[3].strip()
    button = tokens[2].strip()
    log.debug('remote: %s. button: %s' % (remote, button))

    if remote == 'dvd':
        ir_cmd = "irsend -d %s SEND_ONCE %s %s" % (lirc_unix_sock, remote, button)
        exit_code = os.system(ir_cmd)
        log.info('cmd executed: %s. exit code: %s' % (ir_cmd, exit_code))

    if remote == 'Marantz' and button == 'KEY_RECORDER2':
        log.info('Marantz input set to: %s' % button)
        speaker = SwitchSpeaker(log)
        speaker.external()

    if remote == 'Marantz_RC2000x' and button in ('KEY_POWER_OFF','KEY_TUNER', 'KEY_AUX', 'KEY_CD', 'KEY_RECORDER1', 'KEY_PHONO'):
        log.info('Marantz_RC2000x input set to: %s' % button)
        speaker = SwitchSpeaker(log)
        speaker.internal()

    if remote == 'lights':
        if button == 'KEY_1':
            modifier = MAIN_LIGHT
        if button == 'KEY_2':
            modifier = DINING_LIGHT
        if button == 'KEY_3':
            modifier = KITCHEN_LIGHT
        if button == 'KEY_4':
            modifier = CHRISTMAS_LIGHTS
        if button == 'KEY_5':
            modifier = BOX_LIGHT
        if button == 'KEY_6':
            modifier = CORNER_LIGHT
        if button == 'KEY_7':
            modifier = DESK_LIGHT
        if button == 'KEY_8':
            modifier = WINDOW_LIGHT

        if button == 'KEY_VOLUMEUP':
            domoticz.switch_light(modifier, 'On')
        if button == 'KEY_VOLUMEDOWN':
            domoticz.switch_light(modifier, 'Off')

        if button == 'KEY_CHANNELUP':
            domoticz.increment_level(modifier)
        if button == 'KEY_CHANNELDOWN':
            domoticz.decrement_level(modifier)

        log.info('Switch light on. Modifier: %s. Lights remote button: %s' % (modifier, button))
