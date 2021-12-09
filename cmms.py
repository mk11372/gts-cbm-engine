import requests
import pandas as pd

# ==== Manage connection to Priority API ====

def fetch_raw_data():
    r = requests.get("https://csense.wee.co.il/odata/Priority/tabula.ini/csusain/DOCUMENTS_Q", auth=('API', 'Ap123456!'))
    return r.json()

def raw_to_df(raw_json):
    return pd.DataFrame(raw_json['value'])

def run_api_pull():
    service_calls = fetch_raw_data()
    print(raw_to_df(service_calls).head(40))

run_api_pull()
