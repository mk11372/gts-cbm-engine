import pandas as pd
import csv

class Asset:

    def __init__(self, name):
        self.name = name

class TouchPoint(Asset):

    def __init__(self, name):
        super().__init__(name)

class Terminal(Asset):

    def __init__(self, name):
        super().__init__(name)

class Elevator:

    def __init__(self, total_cycles, last_maintenance_date, partial_cycles):
        self.total_cycles = total_cycles
        self.last_maintenance_date = last_maintenance_date
        self.partial_cycles = partial_cycles

class TouchPointElevator(TouchPoint, Elevator):

    def __init__(self, name, side, total_cycles, last_maintenance_date, partial_cycles):
        TouchPoint.__init__(self, name)
        Elevator.__init__(self, total_cycles, last_maintenance_date, partial_cycles)
        self.side = side

class TerminalElevator(TouchPoint, Elevator):

    def __init__(self, name, total_cycles, last_maintenance_date, partial_cycles):
        Terminal.__init__(self, name)
        Elevator.__init__(self, total_cycles, last_maintenance_date, partial_cycles)

assets = pd.read_csv("assets.csv", header=0)

for i in assets.index:
    if "tp" in assets.name[i]:
        print("tp")
    else:
        print("no tp")