import assets
import conditions
import database as db
import pandas as pd
from dateutil import parser
import json

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

def get_asset_history(asset_list):
    data = import_json()
    for x in data:
        for asset in asset_list:
            if "tr" in asset.name and asset.name == x['name']:
                asset.update_maintenance_flag(x['maintenance_flag'])
            if "tp" in asset.name and asset.name == x['name'] and asset.side == x['side']:
                asset.update_maintenance_flag(x['maintenance_flag'])

def get_maintenance_dates(csv="maintenance_dates.csv"):
    """Convert Priority-formatted UTC dates to SQL-friendly strings"""
    last_maintenance_date_df = pd.read_csv("maintenance_dates.csv", header=0)
    last_maintenance_date_df.date = last_maintenance_date_df.date.apply(lambda x: parser.parse(x).strftime("%Y-%m-%d %H:%M:%S"))
    return last_maintenance_date_df

def update__asset_maintenance_date(asset_list, last_maintenance_date_df):
    """Update all assets with their last maintenance dates"""
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
        sql = asset.get_partial_cycles_query()
        partial_cycles_df = db.run_query(cs, sql)
        asset.update_partial_cycles(partial_cycles_df) 
    db.close_cursor(cs)
    db.close_connection(cnn)

def check_conditions(asset_list):
    for asset in asset_list:
        if asset.maintenance_flag == False:
            maintenance_flag_result = conditions.station_belt_condition.check_against_threshold(asset.partial_cycles)
            asset.update_maintenance_flag(maintenance_flag_result)

def export_json(asset_list):
    data = [asset.__dict__ for asset in asset_list]
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

def import_json():
    with open('data.json', 'r') as infile:
        return json.load(infile)
   

def run_program():
    print("Building asset list...")
    asset_list = build_asset_list()
    get_asset_history(asset_list)
    print("Fetching asset data...")
    last_maintenance_date_df = get_maintenance_dates()
    update__asset_maintenance_date(asset_list, last_maintenance_date_df)
    query_db(asset_list)
    check_conditions(asset_list)
    export_json(asset_list)
    print("Asset data ready!")

run_program()


