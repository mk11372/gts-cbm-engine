import pandas as pd

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

    def get_total_cycles_query(self, header_context="", query_context=""):
        """Generate SQL query w/ string literals corresponding to asset type of child classes."""
        sql = f"SELECT MFC_ID, STATION_ID{header_context}, COUNT(*) TOTAL_CYCLES " \
        + "FROM ELEVATOR_MOVEMENT " \
        + f"WHERE ELEVATOR_MOVE = 'up' AND MFC_ID = 'US0002' AND STATION_ID = '{self.name}' {query_context} AND CREATED_AT > '2000-01-01 00:00' " \
        + f"GROUP BY MFC_ID, STATION_ID{header_context} " \
        + "ORDER BY TOTAL_CYCLES DESC"
        return sql

    def get_partial_cycles_query(self, header_context="", query_context=""):
        """Generate SQL query w/ string literals corresponding to asset type of child classes."""
        sql = f"SELECT MFC_ID, STATION_ID{header_context}, COUNT(*) PARTIAL_CYCLES " \
        + "FROM ELEVATOR_MOVEMENT " \
        + f"WHERE ELEVATOR_MOVE = 'up' AND MFC_ID = 'US0002' AND STATION_ID = '{self.name}' {query_context} AND CREATED_AT > '{self.last_maintenance_date}' " \
        + f"GROUP BY MFC_ID, STATION_ID{header_context} " \
        + "ORDER BY PARTIAL_CYCLES DESC"
        return sql

    def update_total_cycles(self, total_cycles_df):
        self.total_cycles = total_cycles_df.iloc[0].TOTAL_CYCLES

    def update_partial_cycles(self, partial_cycles_df):
        self.partial_cycles = partial_cycles_df.iloc[0].PARTIAL_CYCLES

    def update_maintenance_date(self, last_maintenance_date):
        self.last_maintenance_date = last_maintenance_date

class TouchPointElevator(TouchPoint, Elevator):

    def __init__(self, name, side, total_cycles=0, last_maintenance_date=0, partial_cycles=0):
        TouchPoint.__init__(self, name)
        Elevator.__init__(self, total_cycles, last_maintenance_date, partial_cycles)
        self.side = side

    def get_total_cycles_query(self):
        """Fill string literals with touchpoint-specific query parameters"""
        return super().get_total_cycles_query(header_context=", SUBSTATION_ELEVATOR", query_context=f"AND SUBSTATION_ELEVATOR = '{self.side}'")

    def get_partial_cycles_query(self):
        """Fill string literals with touchpoint-specific query parameters"""
        return super().get_partial_cycles_query(header_context=", SUBSTATION_ELEVATOR", query_context=f"AND SUBSTATION_ELEVATOR = '{self.side}'")

class TerminalElevator(Terminal, Elevator):

    def __init__(self, name, total_cycles=0, last_maintenance_date=0, partial_cycles=0):
        Terminal.__init__(self, name)
        Elevator.__init__(self, total_cycles, last_maintenance_date, partial_cycles)

    def get_total_cycles_query(self, header_context="", query_context=""):
        """Fill string literals with terminal-specific query parameters"""
        return super().get_total_cycles_query(header_context, query_context)

    def get_partial_cycles_query(self, header_context="", query_context=""):
        """Fill string literals with terminal-specific query parameters"""
        return super().get_partial_cycles_query(header_context, query_context)