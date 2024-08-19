import glob
import os
from pathlib import Path
import inspect
import requests
from requests.adapters import HTTPAdapter
import ssl
import pandas as pd
import logging
import time
from sqlalchemy import create_engine 
import urllib 

def conxn():
    conn = urllib.parse.quote_plus( 
        'Data Source Name=qrice;' 
        'Driver={ODBC Driver 17 for SQL Server};' 
        'Server=QRICE;' 
        'Database=cepik;' 
        'Trusted_connection=yes;' 
    ) 
    coxn = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn))
    return coxn  

def connect_and_dataload(api_link,params):
    class SSLAdapter(HTTPAdapter):
        def init_poolmanager(self, *args, **kwargs):
            ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            ctx.set_ciphers('DEFAULT@SECLEVEL=1')
            kwargs['ssl_context'] = ctx
            return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

    session = requests.Session()
    session.mount('https://', SSLAdapter())

    request_count = 0
    MAX_REQUESTS = 100

    if request_count >= MAX_REQUESTS:
        log = "API rate limit reached. Waiting for a minute."
        logging.info(log)
        print(log)
        time.sleep(60)
        request_count = 0

    time.sleep(0.05)  # Ensure at most 20 requests per second

    response = session.get(api_link, params=params)

    if response.status_code == 200:
        try:
            data = response.json()  # attempt to parse JSON response
            if 'data' in data:
                df = pd.json_normalize(data['data'])
                log = f"Request successful"
                logging.info(log)
                print(log)
            else:
                print("The key 'data' is not in the response JSON")
        except ValueError as e:
            df.to_csv(data)
            print("Error parsing JSON:", e)
        except Exception as e:
            logging.error(f"Error, failed to retrieve data: {e}")
            print(f"Error, failed to retrieve data: {e}")
            if '429' in str(e):
                    log = "Rate limit reached. Waiting for 60 seconds."
                    logging.warning(log)
                    print(log)
                    time.sleep(60)
                    request_count = 0
            else:
                    log = "An unexpected error occurred. Stopping."
                    logging.error(log)
                    print(log)
    else:
        print("Error, failed to retrieve data:", response.status_code)

    request_count += 1

    return df, data

def to_database(df,table):
    coxn=conxn()
    try:
        df.to_sql(table, con=coxn, schema='dbo', if_exists='replace', index=True)
        print("Data successfully written to SQL database.")
    except Exception as e:
        print("Failed to write data to SQL database:", str(e))

def csv_name():
    caller_frame = inspect.stack()[1]
    caller_file_path_full = os.path.abspath(caller_frame.filename)
    caller_file_path_short = caller_file_path_full[:-3]
    extension = '.csv'
    filename = (f'{caller_file_path_short}{extension}')

    return filename

def check_file(path,name):
        files = glob.glob(os.path.join(path, name))
        return files