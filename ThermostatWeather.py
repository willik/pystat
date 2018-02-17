import urllib.request
import time
import json
import threading

class ThermostatWeather():
    def __init__(self, apiKey, url, latlong, weatherFlags=""):

        # set up for forecast.io api call
        self.apiKey = apiKey
        self.url = url
        self.latlong = latlong
        self.weatherFlags = weatherFlags

        # set up to handle getting daily weather data
        self.lastCheck = time.time()
        self.currentLock = threading.Lock()

        try:
            self.weatherData = self.get_current_data()
        except:
            self.weatherData = None

    def get_current_data(self):
        # get current time in seconds
        currentTime = time.strftime('%s')

        # create the url to fetch from provided settings
        url = self.url + "/" + self.apiKey + "/" + self.latlong + "," +\
              currentTime + "?" + self.weatherFlags

        # request data
        current = urllib.request.urlopen(url).read()

        # parse into dictionary
        weatherData = json.loads(current.decode("utf-8"))

        # daily's only element is an array with only one element... another dictionary...
        # it is silly, just make daily point to the sub dictionary
        weatherData['daily'] = weatherData['daily']['data'][0]

        return weatherData

    def CurrentData(self, type):
        n = 900 # 15 minutes

        # if requesting today's forecast, we do not need such recent queries
        if 'today' == type:
            n = 3600 # 1 hour

        # cache data and only update at intervals
        if n <= int(time.time() - self.lastCheck):
            self.currentLock.acquire()

            self.weatherData = self.get_current_data()

            self.lastCheck = time.time()
            self.currentLock.release()

        return self.weatherData

    def current_weather(self):
        try:
            # extract current weather data from CurrentData
            currently = self.CurrentData('current')['currently']

            # return the apparent temperature and a summary
            return {
                'temperature': round(currently['apparentTemperature'], 1),
                'summary': currently['summary']
            }
        except:
            return None

    def today_forecast(self):
        try:
            # extract today's forcast from CurrentData
            today = self.CurrentData('today')['daily']

            # return a summary of today's weather, the apparent high and low, and the
            # probability of precipitation
            return {
                'summary': today['summary'],
                'apparentTemperatureMax': round(today['apparentTemperatureMax'], 1),
                'apparentTemperatureMin': round(today['apparentTemperatureMin'], 1),
                'precipProbability': today['precipProbability'],
            }
        except:
            return None
