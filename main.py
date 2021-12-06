import assets
import database as db

asset_list = assets.build_asset_list()

cnn = db.open_connection()
cs = db.open_cursor(cnn)

for asset in asset_list:
    sql = asset.get_total_cycles_query()
    df = db.run_query(cs, sql)
    print(df.head())

db.close_cursor(cs)
db.close_connection(cnn)