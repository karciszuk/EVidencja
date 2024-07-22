def connect_and_dataload(api_link,params):
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

    response = session.get(api_link, params=params)

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
    
    return df,data

def to_database(df,coxn,table):
    try:
        df.to_sql(table, con=coxn, schema='dbo', if_exists='replace', index=True)
        print("Data successfully written to SQL database.")
    except Exception as e:
        print("Failed to write data to SQL database:", str(e))

def to_csv(df):
    from pathlib import Path
    import os
    import inspect

    caller_frame = inspect.stack()[1]
    caller_file_path_full = os.path.abspath(caller_frame.filename)
    caller_file_path_short = caller_file_path_full[:-3]
    extension = '.csv'
    filename = (f'{caller_file_path_short}{extension}')

    try:
        df.to_csv(filename,index=False)
        print("Data successfully written to SQL database.")
    except Exception as e:
        print("Failed to write data to SQL database:", str(e))