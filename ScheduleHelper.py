__author__ = 'matt'

class ScheduleEvent():
    def __init__(self, day, time, temperature, mode):
        self.day = int(day)
        self.time = int(time)
        self.temperature = float(temperature)
        self.mode = mode;

class ScheduleHelper():
    def __init__(self):
        self.schedule = {}

    def deserialize_events(self, fileContents):
        if "" != fileContents:
            for line in fileContents.split():

                # split line into days;time;temperature;mode
                top = line.split(";")
                if 3 == len(top):

                    # split days into day,day,...
                    days = top[0].split(",")
                    time = top[1]
                    temperature = top[2]
                    mode = top[3].toLower
                    if mode not in [ "off", "fan", "ac", "heat" ]:
                        mode = "off"

                    # add all events to the schedule
                    try:
                        for day in days:
                            self.add_event(ScheduleEvent(day, time, temperature, mode))
                    except:
                        pass


    def add_event(self, scheduleEvent):
        print("Scheduled event added")

        if scheduleEvent.day not in self.schedule:
            self.schedule[scheduleEvent.day] = [scheduleEvent]
        else:
            events = self.schedule[scheduleEvent.day]
            added = False

            # iterate through the events for this day
            for i in range(0, len(events)):
                difference = events[i].time - scheduleEvent.time

                # if times are within 30 minutes, fail
                if 30 > abs(difference):
                    return events[i]

                if scheduleEvent.time < events[i].time:
                    events.insert(i, scheduleEvent)
                    added = True
                    break

            # check if scheduleEvent has been added
            if not added:
                events.append(scheduleEvent)

        return None

    def check_for_conflict(self, scheduleEvent):
        # check if any events exist for this day
        if scheduleEvent.day in self.schedule:
            events = self.schedule[scheduleEvent.day]

            # iterate through the events for this day
            for event in events:
                difference = event.time - scheduleEvent.time

                # if times are within 30 minutes, fail
                if 30 > abs(difference):
                    return event

        return None


    def delete_event(self, day, time):
        # check if day exists in schedule
        if day in self.schedule:
            for events in self.schedule[day]:

                # check if any events in schedule match time and day
                for i in range(len(events)):
                    if events[i].time == time:
                        event = events[i]
                        del events[i]
                        return event

    def serialize_events(self):
        timeOrganized = []

        # iterate through keys in schedule
        for key in self.schedule:
            for event in self.schedule[key]:
                matched = False
                if 0 < len(timeOrganized):

                    # iterate through all events in a day
                    for group in timeOrganized:

                        # if given event matches a known time, add to that group
                        if group[0].time == event.time \
                                and group[0].temperature == event.temperature:
                            group.append(event)
                            matched = True
                            break

                # else, create a new group
                if not matched:
                    timeOrganized.append([event])

        # convert events grouped by time into days;hour;temperature
        content = ""
        for group in timeOrganized:
            line = ""

            # add all days to the line
            for i in range(len(group)):
                if 0 != i:
                    line += ","
                line += group[i].day

            # add time and temperature, then a \n
            line += ";" + str(group[0].time) + ";" + group[0].temperature + "\n"
            content += line

        # return serialized schedule
        return content
