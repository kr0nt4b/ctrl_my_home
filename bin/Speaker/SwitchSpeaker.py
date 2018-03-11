#!/usr/bin/python2
import serial
from serial import SerialException


class SwitchSpeaker:

    def __init__(self, logger):
        self.logger = logger
        try:
            self.ser = serial.Serial(
                    port='/dev/ttyUSB0',
                    baudrate=9600
            )

            if not self.ser.isOpen():
                self.logger.info("Serialport /dev/ttyUSB0 cannot be opened.")
        except SerialException:
            self.logger.info("Serialport /dev/ttyUSB0 already opened.")

    def internal(self):
        close_1 = "\xff\x03\x01"
        close_2 = "\xff\x04\x01"
        self.ser.write(close_1)
        self.ser.write(close_2)
        self.ser.close()
        self.logger.info("switched to internal speaker")

    def external(self):
        open_1 = "\xff\x03\x00"
        open_2 = "\xff\x04\x00"
        self.ser.write(open_1)
        self.ser.write(open_2)
        self.ser.close()
        self.logger.info("switched to external speaker")
