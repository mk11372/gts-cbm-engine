import requests

# ==== Manage connection to Priority API ====

def fetch_raw_data():
    r = requests.get("https://csense.wee.co.il/odata/Priority/tabula.ini/csusain/DOCUMENTS_Q", auth=('API', 'Ap123456!'))
    return r.json()
