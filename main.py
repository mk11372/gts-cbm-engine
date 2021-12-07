import assets
import database as db
import pandas as pd

def build_asset_list():
    """Generate list of object instances from .csv manifest"""
    assets_manifest = pd.read_csv("assets.csv", header=0)
    asset_list = []
    for i in assets_manifest.index:
        if "tp" in assets_manifest.name[i]:
            for side in ["left", "right"]:
                tp_elevator = assets.TouchPointElevator(assets_manifest.name[i], side)
                asset_list.append(tp_elevator)
        elif "tr" in assets_manifest.name[i]:
            tr_elevator = assets.TerminalElevator(assets_manifest.name[i])
            asset_list.append(tr_elevator)
    return asset_list

def update__asset_maintenance_date(asset_list):
    last_maintenance_date_df = pd.read_csv("maintenance_dates.csv", header=0)
    for i in last_maintenance_date_df.index:
        for asset in asset_list:
            if "tp" in asset.name:
                if f"{asset.name}-{asset.side}" == last_maintenance_date_df.asset[i]:
                    asset.update_maintenance_date(last_maintenance_date_df.date[i])
            elif "tr" in asset.name:
                if asset.name == last_maintenance_date_df.asset[i]:
                    asset.update_maintenance_date(last_maintenance_date_df.date[i])

def query_db(asset_list):
    cnn = db.open_connection()
    cs = db.open_cursor(cnn)
    for asset in asset_list:
        sql = asset.get_total_cycles_query()
        total_cycles_df = db.run_query(cs, sql)
        asset.update_total_cycles(total_cycles_df)
    db.close_cursor(cs)
    db.close_connection(cnn)

def run_program():
    print("Building asset list...")
    asset_list = build_asset_list()
    print("Fetching asset data...")
    update__asset_maintenance_date(asset_list)
    query_db(asset_list)
    print("Asset data ready!")

run_program()





