__author__ = 'matt'

import threading
import time
from GPIOManager import TestGPIOManager
# from RaspberryPiManager import RaspberryPiManager
# from BeagleBoneBlackGPIOManager import BeagleBoneBlackGPIOManager

class ThermostatService(threading.Thread):
    def __init__(self, threadId, name, configuration, fileManager, temperatureReader):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.configuration = configuration
        self.fileManager = fileManager
        self.temperatureReader = temperatureReader
        self.currentMode = "off"
        self.currentTemperature = 70.0
        self.manager = TestGPIOManager(configuration)
        # self.manager = RaspberryPiManager(configuration)
        # self.manager = BeagleBoneBlackGPIOManager(configuration)

    def run(self):
        print("Starting service")
        self.turn_off_heat()
        self.turn_off_ac()

        #comment for testing
        #time.sleep(300)

        self.turn_off_fan()

        while True:
            print(time.strftime("%H:%M:%S ") + "thermostat service polling...")

            # check current
            newValues = self.fileManager.read_current()

            try:
                newMode = newValues["mode"]
                newTemperature = newValues["temperature"]

                # if mode is changing
                if newMode != self.currentMode:

                    # if new mode is off
                    if "off" == newMode:
                        # turn off unit

                        # if currently fan, simply turn off the fan
                        if "fan" == self.currentMode:
                            self.turn_off_fan()

                        # else, turn off heat or ac, wait 5 minutes, then turn off fan
                        else:
                            if "heat" == self.currentMode:
                                self.turn_off_heat()
                            elif "ac" == self.currentMode:
                                self.turn_off_ac()

                            time.sleep(300)
                            self.turn_off_fan()

                    elif "fan" == newMode:
                        self.turn_on_fan()
                        if "heat" == self.currentMode:
                            self.turn_off_heat()
                        elif "ac" == self.currentMode:
                            self.turn_off_ac()

                        time.sleep(300)

                    elif "heat" == self.currentMode:
                        self.turn_off_heat()
                        time.sleep(300)
                    elif "ac" == self.currentMode:
                        self.turn_off_ac()
                        time.sleep(300)
            except:
                #TODO: handle an error in mode changing
                # error! maybe try handling at some point, but first just turn off
                # everything except the fan.
                self.turn_on_fan()
                self.turn_off_heat()
                self.turn_off_ac()

            # check current
            newValues = self.fileManager.read_current()
            self.currentMode = newValues["mode"]
            self.currentTemperature = round(float(newValues["temperature"]), 1)

            temperature = self.temperatureReader.CurrentTemperature()
            if "heat" == self.currentMode:
                self.turn_off_ac()
                if temperature < self.currentTemperature -\
                        self.configuration.inactiveHysteresis:
                    if "heat" not in self.configuration.running:
                        self.turn_on_fan()
                        self.turn_on_heat()
                elif temperature > self.currentTemperature +\
                        self.configuration.activeHysteresis:
                    if "heat" in self.configuration.running:
                        self.turn_off_heat()
                        time.sleep(300)
                        self.turn_off_fan()

            elif "ac" == self.currentMode:
                self.turn_off_heat()
                if temperature > self.currentTemperature +\
                        self.configuration.inactiveHysteresis:
                    if "ac" not in self.configuration.running:
                        self.turn_on_fan()
                        self.turn_on_ac()
                elif temperature < self.currentTemperature -\
                        self.configuration.activeHysteresis:
                    if "ac" in self.configuration.running:
                        self.turn_off_ac()
                        time.sleep(300)
                        self.turn_off_fan()

            elif "fan" == self.currentMode:
                self.turn_on_fan()
                self.turn_off_heat()
                self.turn_off_ac()

            time.sleep(5)

#TODO: create another helper to manipulate GPIO ports appropriately
    def turn_off_fan(self):
        if "fan" in self.configuration.running:
            self.configuration.running.remove("fan")
            self.manager.turn_off_fan()

    def turn_on_fan(self):
        if "fan" not in self.configuration.running:
            self.configuration.running.append("fan")
            self.manager.turn_on_fan()

    def turn_off_ac(self):
        if "ac" in self.configuration.running:
            self.configuration.running.remove("ac")
            self.manager.turn_off_ac()

    def turn_on_ac(self):
        if "fan" not in self.configuration.running:
            self.configuration.running.append("fan")
            self.manager.turn_on_fan()
        if "ac" not in self.configuration.running:
            self.configuration.running.append("ac")
            self.manager.turn_on_ac()

    def turn_off_heat(self):
        if "heat" in self.configuration.running:
            self.configuration.running.remove("heat")
            self.manager.turn_off_heat()

    def turn_on_heat(self):
        if "fan" not in self.configuration.running:
            self.configuration.running.append("fan")
            self.manager.turn_on_fan()
        if "heat" not in self.configuration.running:
            self.configuration.running.append("heat")
            self.manager.turn_on_heat()
