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

def run_program():
    print("Building asset list...")
    asset_list = build_asset_list()
    print("Fetching asset data...")
    cnn = db.open_connection()
    cs = db.open_cursor(cnn)
    for asset in asset_list:
        sql = asset.get_total_cycles_query()
        total_cycles_df = db.run_query(cs, sql)
        asset.update_total_cycles(total_cycles_df)
    db.close_cursor(cs)
    db.close_connection(cnn)
    print("Asset data ready!")

run_program()

