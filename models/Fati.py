from models.valve import Valve
import db
from sqlalchemy.sql import func

class Fati(db.Model):

    __tablename__ = "fatis"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(125), nullable=False)

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
