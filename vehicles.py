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
from ConnectAndDataload import connect_and_dataload, to_database
from conxn import coxn

api_link = "https://api.cepik.gov.pl/pojazdy"
voivodeship = 0
params={
        "wojewodztwo": voivodeship,
        "data-od": "20100101"
        }
table = 'CepikApiData'


df, data = connect_and_dataload(api_link,params)

df = pd.json_normalize(data['data'])    
df.columns = df.columns.str.replace('attributes.','', regex=True)
df.columns = df.columns.str.replace('-', '_', regex=True)
df = df.drop(columns=['links.self'])

to_database(df,coxn,table)