# !/usr/bin/python
from datetime import datetime, timedelta
import os

from bin.heater.NextMoment import NextMoment
from LogClient import LogClient


class Interval:

    def __init__(self, logger):
        self.logger = logger
        self.heat_file = "heat.txt"
        self.heat_duration = "heat.txt"
        self.check_times = ["02:00", "06:00", "07:00", "14:00", "21:00", "23:00"]

    def __read_configured(self):
        if not os.path.exists(self.heat_file):
            return False

        with open(self.heat_file, "r") as file:
            return file.readline().split(" ")

    def heater_set(self):
        when = self.__read_configured()
        return when[0] if when else False

    def duration(self):
        duration = self.__read_configured()
        return duration[1] if duration else 15

    def fixed_when(self):
        now = datetime.now()

        next_time = self.__configured_time(now, self.check_times[0]) - now

        if next_time.days == -1:
            next_time = (next_time + timedelta(days=1))

        time_left = None

        for check_time in self.check_times:
            check_time = self.__configured_time(now, check_time)
            time_left = check_time - now
            if time_left.days == -1:
                time_left = (time_left + timedelta(days=1))

            if time_left < next_time:
                next_time = time_left

        if time_left is None:
            self.logger.info('no fixed interval. Set interval to 1 hour')
            return 3600 * 24 * 1000

        self.logger.info('Reporting fixed interval. Time to next moment is %s' % time_left)
        return time_left.seconds * 1000

    def __check_when(self):
        now = datetime.now()

        when = self.heater_set()
        if not when:
            self.logger.info('heater file %s does not exist. try fixed interval' % self.heat_file)
            return self.fixed_when()

        check_time = self.__configured_time(now, when)
        result = check_time - now
        if result.days == -1:
            result = (result + timedelta(days=1)).seconds * 1000
            self.logger.info('Reporting configured time. Time to next moment is tomorrow at %s' % result)
            return result
        if result.days == 0:
            self.logger.info('Reporting configured time. Time to next moment is today at %s' % result)
            return result.seconds * 1000

    def clear_file(self):
        os.remove(self.heat_file)

    @staticmethod
    def __configured_time(now, check):
        configured_time = '%s-%s-%s-%s' % (str(now.year), str(now.month), str(now.day), check)
        return datetime.strptime(configured_time, "%Y-%m-%d-%H:%M")

    def get_next_moment(self):
        duration = interval.duration()
        return NextMoment("on", self.__check_when(), duration)


if __name__ == "__main__":
    log = LogClient("heater_server")
    interval = Interval(log)
    test = interval.get_next_moment()
    test = None
