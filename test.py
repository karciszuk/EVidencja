import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl
import pandas as pd
from pandas import json_normalize
import sqlalchemy as sa
from conxn import coxn
import json
from datetime import datetime

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

session = requests.Session()

session.mount('https://', SSLAdapter())

print(session)

response = session.get("https://api.cepik.gov.pl/pojazdy", params={
    "wojewodztwo": "30",
    "data-od": "20100101"
})

print(response)

if response.status_code == 200:
    try:
        data = response.json()  # attempt to parse JSON response
        if 'data' in data:
            df = pd.json_normalize(data['data'])
            print(df.head())  # display the first few rows of the DataFrame
        else:
            print("The key 'data' is not in the response JSON")
    except ValueError as e:
        print("Error parsing JSON:", e)
else:
    print("Failed to retrieve data:", response.status_code)

df = pd.json_normalize(data['data'])    
df.columns = df.columns.str.replace('attributes.','', regex=True)
df.columns = df.columns.str.replace('-', '_', regex=True)
df = df.drop(columns=['links.self'])

print(df)