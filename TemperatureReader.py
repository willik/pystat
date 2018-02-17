__author__ = 'matt'

import threading
import time

# A static class that provides the current temperature to a requestor.  Updates the
# temperature every 10 seconds
class TemperatureReader():
    def __init__(self):
        self.currentTemperature = self.get_current_temperature()
        self.lastCheck = time.time()
        self.currentLock = threading.Lock()

    def get_current_temperature(self):
        # check thermometer
        try:
            f = open("/sys/bus/w1/devices/28-0000041117ab/w1_slave")
            f.readline()
            line = f.readline()
            split = line.split("=")

            temperature = float(split[1]) / 1000
            fahrenheit = round((temperature * 1.8) + 32, 1)

            f.close()
            return fahrenheit
        except:
            print("reading thermometer failed, returning -1000")
            return -1000

    def CurrentTemperature(self):
        if 10 <= time.time() - self.lastCheck:
            self.currentLock.acquire()
            self.currentTemperature = self.get_current_temperature()
            self.lastCheck = time.time()
            self.currentLock.release()

        return self.currentTemperature
