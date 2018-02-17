__author__ = 'matt'

import RPi.GPIO as rpiGPIO
from GPIOManager import GPIOManager


class RaspberryPiManager(GPIOManager):
    def __init__(self, configuration):
        GPIOManager.__init__(self, configuration)
        rpiGPIO.setmode(rpiGPIO.BCM)

    def turn_off_fan(self):
        pin = int(self.configuration.fanPin)
        try:
            rpiGPIO.output(pin, False)
        except:
            rpiGPIO.setup(pin, rpiGPIO.OUT)
            rpiGPIO.output(pin, False)

    def turn_on_fan(self):
        pin = int(self.configuration.fanPin)
        try:
            rpiGPIO.output(pin, True)
        except:
            rpiGPIO.setup(pin, rpiGPIO.OUT)
            rpiGPIO.output(pin, True)

    def turn_off_ac(self):
        pin = int(self.configuration.acPin)
        try:
            rpiGPIO.output(pin, False)
        except:
            rpiGPIO.setup(pin, rpiGPIO.OUT)
            rpiGPIO.output(pin, False)

    def turn_on_ac(self):
        pin = int(self.configuration.acPin)
        try:
            rpiGPIO.output(pin, True)
        except:
            rpiGPIO.setup(pin, rpiGPIO.OUT)
            rpiGPIO.output(pin, True)

    def turn_off_heat(self):
        pin = int(self.configuration.heatPin)
        try:
            rpiGPIO.output(pin, False)
        except:
            rpiGPIO.setup(pin, rpiGPIO.OUT)
            rpiGPIO.output(pin, False)

    def turn_on_heat(self):
        pin = int(self.configuration.heatPin)
        try:
            rpiGPIO.output(pin, True)
        except:
            rpiGPIO.setup(pin, rpiGPIO.OUT)
            rpiGPIO.output(pin, True)
