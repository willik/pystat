__author__ = 'matt'

class ThermostatConfiguration:
    def __init__(self):
        self.heatPin = -1
        self.acPin = -1
        self.fanPin = -1

        self.activeHysteresis = 2.0
        self.inactiveHysteresis = 2.0
        self.minimumTemperature = 50
        self.maximumTemperature = 80

        self.emailAlerts = False
        self.email = ""
        self.errorThreshold = 0

        self.running = []

        self.weatherurl = ""
        self.weatherAPIKey = ""
        self.latlong = ""
        self.weatherFlags = ""
