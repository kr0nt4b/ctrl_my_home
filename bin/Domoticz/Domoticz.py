import urllib2
import base64
import json


class DomoticzClient:

    def __init__(self, logger):
        self.base = "https://domoticz.totalize.nl/json.htm?username=a3IwbnQ0Ygo=&password=c2lsOEhlZWQK"
        #self.on_off_cmd = self.base + "&type=command&param=switchlight&idx=%s&switchcmd=%s"
        self.logger = logger

    def get_device_info(self, idx):
        cmd_list = self.base + "&type=devices&rid=%s" % (idx)
        response = self.send_get(cmd_list)
        light_json = json.loads(response)
        current = light_json['result'][0]['Level']
        max_level = light_json['result'][0]['MaxDimLevel']
        self.logger.info("Level: %s. Max: %s" % (current, max_level))
        return current, max_level

    def increment_level(self, idx):
        current, max_level = self.get_device_info(idx)
        increment = current + 10
        if increment > max_level:
            increment = max_level
        self.set_level(idx, increment)

    def decrement_level(self, idx):
        current = self.get_device_info(idx)
        decrement = current - 10
        if decrement < 0:
            decrement = 0
        self.set_level(idx, decrement)

    def set_level(self, idx, level):
        cmd = self.base + "&type=command&param=switchlight&idx=%s&switchcmd=Set%%20Level&level=%s" % (idx, level)
        response = self.send_get(cmd)
        self.logger.info("set_level. response: %s" % response)

    def switch_light(self, idx, on_off):
        cmd = self.base + "&type=command&param=switchlight&idx=%s&switchcmd=%s" % (idx, on_off)
        response = self.send_get(cmd)
        self.logger.info("switch_light. response: %s" % response)

    # def internal_speaker(self):
    #     cmd = self.on_off_cmd % (48, "On")
    #     print("internal_speaker. response: %s" % response)
    #     response = self.send_get(cmd)
    #     self.logger.info("switch to internal speaker. response: %s" % response)
    #
    # def external_speaker(self):
    #     cmd = self.on_off_cmd % (48, "Off")
    #     print("external_speaker. response: %s" % response)
    #     response = self.send_get(cmd)
    #     self.logger.info("switch to external speaker. response: %s" % response)
    #
    # def tv_off(self):
    #     cmd = self.on_off_cmd % (62, "Off")
    #     print("external_speaker. response: %s" % response)
    #     response = self.send_get(cmd)
    #     self.logger.info("tv switched off. response: %s" % response)

    @staticmethod
    def send_get(url):
        request = urllib2.Request(url)
        base64string = base64.b64encode('%s:%s' % ("kr0nt4b", "sil!5Heed"))
        request.add_header("Authorization", "Basic %s" % base64string)
        return urllib2.urlopen(request).read()
