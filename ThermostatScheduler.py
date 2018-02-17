__author__ = 'matt'

import threading
import time
import ScheduleHelper

class ThermostatScheduler(threading.Thread):
    def __init__(self, threadId, name, configuration, fileManager, temperatureReader):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.configuration = configuration
        self.fileManager = fileManager
        self.temperatureReader = temperatureReader
        self.scheduleHelper = ScheduleHelper.ScheduleHelper()
        fileManager.scheduleHelper = self.scheduleHelper

    def run(self):
        self.scheduleHelper.deserialize_events(self.fileManager.read_schedule())

        while True:

            # get the day of the week as an int 0 = Sunday
            day = int(time.strftime("%w"))

            # check if there are any scheduled events for today
            if day in self.scheduleHelper.schedule:

                # get current hour and minute and store as an int HHMM
                hour = int(time.strftime("%H"))
                minute = int(time.strftime("%M"))
                currentTime = hour * 100 + minute

                # iterate through today's scheduled events
                for event in self.scheduleHelper.schedule[day]:

                    # get the time difference from now to the event
                    difference = event.time - currentTime

                    # check if the event is within 5 minutes of now
                    if 5 > abs(difference):
                        print("Event found\n\t" + event.mode + "\n\t" + event.temperature)

                        # wait for the event time if it has not already passed
                        if 0 < difference:
                            time.sleep(difference * 60)

                        self.fileManager.write_current(event.mode, event.temperature)
                        break

            # wait 5 minutes, then check the schedule again
            time.sleep(300)
