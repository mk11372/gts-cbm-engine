import pandas as pd

assets_manifest = pd.read_csv("assets.csv", header=0)

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
        + f"WHERE ELEVATOR_MOVE = 'up' AND MFC_ID = 'US0002' AND STATION_ID = '{self.name}' {query_context} AND CREATED_AT > '2015-01-01 00:00' " \
        + f"GROUP BY MFC_ID, STATION_ID{header_context} " \
        + "ORDER BY TOTAL_CYCLES DESC"
        return sql

class TouchPointElevator(TouchPoint, Elevator):

    def __init__(self, name, side, total_cycles=0, last_maintenance_date=0, partial_cycles=0):
        TouchPoint.__init__(self, name)
        Elevator.__init__(self, total_cycles, last_maintenance_date, partial_cycles)
        self.side = side

    def get_total_cycles_query(self):
        return super().get_total_cycles_query(header_context=", SUBSTATION_ELEVATOR", query_context=f"AND SUBSTATION_ELEVATOR = '{self.side}'")

class TerminalElevator(Terminal, Elevator):

    def __init__(self, name, total_cycles=0, last_maintenance_date=0, partial_cycles=0):
        Terminal.__init__(self, name)
        Elevator.__init__(self, total_cycles, last_maintenance_date, partial_cycles)

    def get_total_cycles_query(self, header_context="", query_context=""):
        return super().get_total_cycles_query(header_context, query_context)

def build_asset_list():
    asset_list = []
    for i in assets_manifest.index:
        if "tp" in assets_manifest.name[i]:
            for side in ["left", "right"]:
                tp_elevator = TouchPointElevator(assets_manifest.name[i], side)
                asset_list.append(tp_elevator)
        elif "tr" in assets_manifest.name[i]:
            tr_elevator = TerminalElevator(assets_manifest.name[i])
            asset_list.append(tr_elevator)
    return asset_list

# asset_list = build_asset_list()
# test = asset_list[1].get_total_cycles_query()
# print(test)