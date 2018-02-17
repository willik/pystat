__author__ = 'matt'

import sqlite3
import time

# defines the sql that creates the current data table
CREATE_TABLE_current_data = 'CREATE TABLE current_data' \
                            '(time                  INTEGER PRIMARY KEY,' \
                            ' indoor_temperature    REAL NOT NULL,' \
                            ' target_temperature    REAL NOT NULL,' \
                            ' outdoor_temperature   REAL,' \
                            ' target_mode           TEXT NOT NULL,' \
                            ' heat_running          INTEGER NOT NULL,' \
                            ' ac_running            INTEGER NOT NULL,' \
                            ' fan_running           INTEGER NOT NULL' \
                            ')'

#CREATE_TABLE_settings_change = 'CREATE TABLE settings_change' \
                               # '(time               INTEGER PRIMARY KEY,' \
                               # ' target_temperature REAL NOT NULL' \
                               # ' target_mode        TEXT NOT NULL' \
                               # ')'

'''
ThermostatDatabase is a static utility class that allows services to log data to an
sqlite3 database
'''
class ThermostatDatabase():

    # ThermostatMain will provide the database name
    def __init__(self, databaseName):
        self.databaseName = databaseName

    # to be called when the database does not exist
    def create(self):
        if self.databaseName is not None:
            connection = sqlite3.connect(self.databaseName)

            c = connection.cursor()
            c.execute(CREATE_TABLE_current_data)
            #c.execute(CREATE_TABLE_settings_change)

    def check_current_table(self):
        try:
            connection = sqlite3.connect(self.databaseName)

            c = connection.cursor()
            c.execute("SELECT * FROM current_data")

            return False
        except:
            return True

    # takes current data in and logs it into the database
    def insert_current_data(self, indoorTemperature, targetTemperature,
                            outdoorTemperature, targetMode, heatRunning, acRunning,
                            fanRunning):

        if self.check_current_table():
            self.create()

        indoorTemperature = str(indoorTemperature)
        targetTemperature = str(targetTemperature)

        heatRunning = '1' if heatRunning else '0'
        acRunning = '1' if acRunning else '0'
        fanRunning = '1' if fanRunning else '0'

        sql = 'INSERT INTO current_data VALUES( ?, ?, ?, ?, ?, ?, ?, ?)'

        try:
            connection = sqlite3.connect(self.databaseName)

            c = connection.cursor()
            c.execute(sql, (time.strftime("%s"), indoorTemperature, targetTemperature,
                      outdoorTemperature, targetMode, heatRunning, acRunning, fanRunning))

            connection.commit()
        finally:
            connection.close()
