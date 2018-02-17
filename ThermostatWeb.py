__author__ = 'matt'

import threading
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, \
    flash, jsonify

class ThermostatWeb(threading.Thread):
    def __init__(self, threadID, name, configuration, fileManager,
                 temperatureReader, weather):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.configuration = configuration
        self.fileManager = fileManager
        self.temperatureReader = temperatureReader
        self.weather = weather

        self.app = Flask(__name__)

        # prepare method to call when / is navigated to
        @self.app.route("/", methods=['GET', 'POST'])
        def index():
            if request.args.get("mode") is not None \
                    and request.args.get("temperature"):
                mode = request.args.get("mode")
                temperature = round(float(request.args.get("temperature")), 1)
                self.fileManager.write_current(mode, temperature)

            if 'POST' == request.method:
                data = request.form
                mode = data["mode"]
                temperature = round(float(data["temperature"]), 1)

                self.fileManager.write_current(mode, temperature)

            return self.webpage_helper(render_template, 'request')

        @self.app.route("/update")
        def update():
            return self.webpage_helper(jsonify, 'update')

    # take a function and gather necessary data for the web ui, then call the function
    # with the gathered data an an input and return the result
    def webpage_helper(self, function, type):
        # get current settings and house temperature
        current = self.fileManager.read_current()
        currentTemperature = self.temperatureReader.CurrentTemperature()
        heatRunning = "heat" in self.configuration.running
        acRunning = "ac" in self.configuration.running
        fanRunning = "fan" in self.configuration.running


        # get weather
        currentWeather = self.weather.current_weather()
        today = self.weather.today_forecast()

        # handle a lack of weather api data
        if currentWeather is None or today is None:
            currentWeatherTemp = currentWeatherSummary = todaySummary = todayMax =\
                todayMin = todayPrecipProbability = None
        else:
            currentWeatherTemp = currentWeather['temperature']
            currentWeatherSummary = currentWeather['summary']

            todaySummary = today['summary']
            todayMax = today['apparentTemperatureMax']
            todayMin = today['apparentTemperatureMin']
            todayPrecipProbability = today['precipProbability']

        # check if we should include 'index.html' in the function call
        if 'update' == type:
            return function(currentMode=current["mode"],
                            currentTarget=current["temperature"],
                            currentTemperature=currentTemperature,
                            heatRunning=heatRunning,
                            acRunning=acRunning,
                            fanRunning=fanRunning,
                            currentWeatherTemp=currentWeatherTemp,
                            currentWeatherSummary=currentWeatherSummary,
                            todaySummary=todaySummary,
                            todayMax=todayMax,
                            todayMin=todayMin,
                            todayPrecipProbability=todayPrecipProbability)

        return function('index.html',
                        currentMode=current["mode"],
                        currentTarget=current["temperature"],
                        currentTemperature=currentTemperature,
                        heatRunning=heatRunning,
                        acRunning=acRunning,
                        fanRunning=fanRunning,
                        currentWeatherTemp=currentWeatherTemp,
                        currentWeatherSummary=currentWeatherSummary,
                        todaySummary=todaySummary,
                        todayMax=todayMax,
                        todayMin=todayMin,
                        todayPrecipProbability=todayPrecipProbability)

    def run(self):
        self.app.run()
