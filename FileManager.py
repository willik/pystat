__author__ = 'matt'

import threading
from ScheduleHelper import ScheduleEvent
from ThermostatConfiguration import ThermostatConfiguration

class FileManager():
    def __init__(self, configurationFileName, currentFileName, scheduleFileName):
        self.configurationFileName = configurationFileName
        self.currentFileName = currentFileName
        self.scheduleFileName = scheduleFileName
        self.configuration = None
        self.scheduleHelper = None

        self.configurationLock = threading.Lock()
        self.currentLock = threading.Lock()
        self.scheduleLock = threading.Lock()

    def read_configuration(self):
        self.configurationLock.acquire()
        configurationFile = open(self.configurationFileName)

        if configurationFile.readable():
            self.configuration = ThermostatConfiguration()
            for line in configurationFile:
                line = line.strip()
                if "" != line and "#" != line[0]:
                    pair = line.split()
                    if 1 < len(pair):
                        self.set_configuration_option(pair[0], pair[1], self.configuration)

        configurationFile.close()
        self.configurationLock.release()
        return self.configuration

    def read_current(self):
        self.currentLock.acquire()
        currentFile = open(self.currentFileName)
        current = None

        if currentFile.readable():
            current = {}
            for line in currentFile:
                line = line.strip()
                if "" != line and "#" != line[0]:
                    pair = line.split()
                    if 1 < len(pair) and ("mode" == pair[0] or "temperature" == pair[0]):
                        current[pair[0]] = pair[1]

        self.currentLock.release()
        currentFile.close()
        return current

    def write_current(self, mode, temperature):
        self.currentLock.acquire()
        # ensure values being written are valid
        if mode not in [ "off", "fan", "ac", "heat" ]:
            mode = "off"
        if temperature < self.configuration.minimumTemperature:
            temperature = self.configuration.minimumTemperature
        elif temperature > self.configuration.maximumTemperature:
            temperature = self.configuration.maximumTemperature

        currentFile = open(self.currentFileName, "w")

        if currentFile.writable():
            currentFile.write("mode " + str(mode) + "\ntemperature " + str(temperature))

        self.currentLock.release()
        currentFile.close()

    def read_schedule(self):
        scheduleFileContents = ""
        self.scheduleLock.acquire()

        scheduleFile = open(self.scheduleFileName)
        if scheduleFile.readable():
            scheduleFileContents = scheduleFile.read()

        self.scheduleLock.release()
        return scheduleFileContents

    def add_event(self, day, time, temperature):
        if self.scheduleHelper is not None:
            try:
                event = self.scheduleHelper.add_event(
                    ScheduleEvent(day, time, temperature))
                if event is None:
                    self.write_schedule(self.scheduleHelper.serialize_events())
                return event
            except:
                pass
        return None

    def delete_event(self, day, time):
        if self.scheduleHelper is not None:
            try:
                return self.scheduleHelper.delete_event(day, time)
            except:
                pass
        return None

    def write_schedule(self, scheduleContents):
        self.scheduleLock.acquire()

        scheduleFile = open(self.scheduleFileName, "w")
        if scheduleFile.writable():
            scheduleFile.write(scheduleContents)

        self.scheduleLock.release()

    def set_configuration_option(self, option_name, option_value, configuration):
        if "heat_pin" == option_name:
            configuration.heatPin = option_value
        elif "ac_pin" == option_name:
            configuration.acPin = option_value
        elif "fan_pin" == option_name:
            configuration.fanPin = option_value
        elif "active_hysteresis" == option_name:
            configuration.activeHysteresis = option_value
        elif "inactive_hysteresis" == option_name:
            configuration.inactiveHysteresis = option_value
        elif "email_alerts" == option_name:
            configuration.emailAlerts = ("true" == option_value.lower())
        elif "email" == option_name:
            configuration.email = option_value
        elif "error_threshold" == option_name:
            configuration.errorThreshold = option_value
        elif "weather_url" == option_name:
            configuration.weatherurl = option_value
        elif "weather_api_key" == option_name:
            configuration.weatherAPIKey = option_value
        elif "lat_long" == option_name:
            configuration.latlong = option_value
