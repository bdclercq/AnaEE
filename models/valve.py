from models.Configuration import Config


class Valve:

    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.configs = []

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_number(self):
        return self.number

    def configure(self, year, month, day, hour, minute, second):
        conf = Config(year, month, day, hour, minute, second)
        self.configs.append(conf)

    def get_confs(self):
        return self.configs
