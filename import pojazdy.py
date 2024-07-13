import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl
import pandas as pd
from pandas import json_normalize
import sqlalchemy as sa
from conxn import coxn
import json

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', SSLAdapter())

response = session.get("https://api.cepik.gov.pl/pojazdy", params={
    "wojewodztwo": "30",
    "data-od": "20190101",
    "data-do": "20190131"
})

if response.status_code == 200:
    data = response.json()
    #print(data)
else:
    print("Failed to retrieve data:", response.status_code)

df = pd.json_normalize(data['data'])
df.columns = df.columns.map(str)
df.columns = df.columns.str.replace('attributes.','', regex=True)
df.columns = df.columns.str.replace('-', '_', regex=True)
df = df.drop(columns=['links.self'])

try:
    df.to_sql('CepikApiData', con=coxn, schema='dbo', if_exists='replace', index=True)
    print("Data successfully written to SQL database.")
except Exception as e:
    print("Failed to write data to SQL database:", str(e))