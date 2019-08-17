from harmony.client import Client
import time
from threading import Thread

ACTIVITY_FILE = '/tmp/harmony'


class HarmonyChecker(Thread):

    def __init__(self, logger, callback):
        Thread.__init__(self)
        self.activity = None
        self.stop_thread = False
        self.log = logger
        self.callback = callback

    @staticmethod
    def write_current_activity(activity):
        timestamp = int(time.time())
        with open(ACTIVITY_FILE, 'w') as harmonyStateFile:
            harmonyStateFile.write(str(timestamp) + ' ' + activity)

    def get_last_activity(self):
        last_timestamp, last_activity = self.read_last_activity()
        current_timestamp = int(time.time())
        seconds_ago = current_timestamp - int(last_timestamp)
        self.log.debug(seconds_ago)

        if seconds_ago > 10:
            return "Unknown"

        return last_activity

    @staticmethod
    def read_last_activity():
        with open(ACTIVITY_FILE, 'r') as reader:
            line = reader.readline()
            last_timestamp, last_activity = line.split(' ')

        if last_timestamp is None:
            last_timestamp = 0
        if last_activity is None:
            last_activity = 'Unknown'

        return last_timestamp, last_activity

    def start(self):

        self.log.info("start thread: run_harmony_checker")
        while True:
            self.activity = self.get_current_activity()

            if self.activity is None:
                self.activity = 'PowerOff'

            self.write_current_activity(self.activity)

            last_timestamp, last_activity = self.read_last_activity()
            if last_activity != self.activity:
                self.callback(self.activity)

            for i in range(0, 50):
                time.sleep(0.1)
                if self.stop_thread:
                    break
            if self.stop_thread:
                break
        self.log.info("stop thread: run_harmony_checker")

    def stop(self):
        self.stop_thread = True

    def get_current_activity(self):
        try:
            harmony_client = Client('192.168.4.186')
            self.activity = harmony_client.get_current_activity_name()
            harmony_client.close()
            self.log.debug('activity: ' + self.activity)
            return self.activity
        except Exception as exception:
            self.log.info('exception occurred: ' + str(exception))
        return ""
