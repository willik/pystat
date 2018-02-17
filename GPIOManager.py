__author__ = 'matt'


class GPIOManager():
    def __init__(self, configuration):
        self.configuration = configuration

    def turn_off_fan(self):
        pass

    def turn_on_fan(self):
        pass

    def turn_off_ac(self):
        pass

    def turn_on_ac(self):
        pass

    def turn_off_heat(self):
        pass

    def turn_on_heat(self):
        pass


class TestGPIOManager(GPIOManager):
    def __init__(self, configuration):
        GPIOManager.__init__(self, configuration)

    def turn_off_fan(self):
        # turn off the fan
        print("turn fan pin off")

    def turn_on_fan(self):
        # turn on the fan
        print("turn fan pin on")

    def turn_off_ac(self):
        # turn off the ac
        print("turn ac pin off")

    def turn_on_ac(self):
        # turn on the ac
        print("turn ac pin on")

    def turn_off_heat(self):
        # turn off the heat
        print("turn heat pin off")

    def turn_on_heat(self):
        # turn on the heat
        print("turn heat pin on")
