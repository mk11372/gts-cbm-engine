import pandas as pd
import snowflake.connector

class Asset:

    def __init__(self, name):
        self.name = name

    def open_snowflake_connection(self):

        # Configuration parameters
        cnn = snowflake.connector.connect (
        user='MICHAELK',
        password='nEKZUgX4wy7bUj6',
        account='fa82594.us-central1.gcp',
        warehouse='CSR_DB_LOAD',
        database='CSR_DB',
        schema='CSR_RAW'
        )

        return cnn

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

    def __init__(self, name, side, total_cycles=0, last_maintenance_date=0, partial_cycles=0):
        TouchPoint.__init__(self, name)
        Elevator.__init__(self, total_cycles, last_maintenance_date, partial_cycles)
        self.side = side

class TerminalElevator(TouchPoint, Elevator):

    def __init__(self, name, total_cycles=0, last_maintenance_date=0, partial_cycles=0):
        Terminal.__init__(self, name)
        Elevator.__init__(self, total_cycles, last_maintenance_date, partial_cycles)

# assets = pd.read_csv("assets.csv", header=0)

# for i in assets.index:
#     if "tp" in assets.name[i]:
#         TouchPointElevator(assets.name[i])
#     else:

