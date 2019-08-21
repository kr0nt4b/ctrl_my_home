#!/usr/bin/env python
from pyharmony import client as harmony_client


class HarmonyClient:

    harmony_c = None

    def __init__(self, ip):
        self.ip = ip
        if self.harmony_c is None:
            self.harmony_c = harmony_client.create_and_connect_client(self.ip, '5222')
            self.harmony_c.auto_reconnect = True
            self.config = self.harmony_c.get_config()

    def start_activity(self, activity):
        for config_item in self.config['activity']:
            if config_item['label'] == activity:
                self.harmony_c.start_activity(config_item['id'])
                break

    def get_current_activity_name(self):
        activity = self.harmony_c.get_current_activity()

        for config_item in self.config['activity']:
            if int(config_item['id']) == activity:
                return config_item['label']
        return ""

    def send_amp_command(self, command, device='Versterker'):
        self.send_device_command(command, device)

    def send_device_command(self, command, device):
        for config_item in self.config['device']:
            if config_item['label'] == device:
                device_id = config_item['id']
                self.harmony_c.send_command(device_id, command)

    def close(self):
        self.harmony_c.disconnect()


#if __name__ == "__main__":
    #client = Client('192.168.88.186')
    #client.start_activity("CD's Luisteren")
    #client.start_activity("PowerOff")
    #client.start_activity("Music")
    #client.send_amp_command('PowerOn')
    #client.send_amp_command('VolumeDown')
    #client.close()
