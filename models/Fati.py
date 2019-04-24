from models.valve import Valve


class Fati:

    def __init__(self, name, number):
        self.number = number
        self.name = name
        self.valves = []
        for i in range(8):
            name = "valve_"
            name += str(i)
            self.valves.append(Valve(name, i))

    def get_name(self):
        return self.name

    def get_number(self):
        return self.number

    def __str__(self):
        return self.name

    def get_valves(self):
        return self.valves

    def get_valve(self, value):
        return self.valves[value]
