import pandas as pd
from main import connect_and_dataload
import time
from datetime import datetime
import glob
import os
import re
import logging

# Configure logging
logging.basicConfig(
        filename='docs/api_requests.log', 
        level=logging.INFO, 
        format='%(asctime)s %(levelname)s:%(message)s')

def check_file(path,name):
        files = glob.glob(os.path.join(path, name))
        return files

api_link = "https://api.cepik.gov.pl/pojazdy"
table = 'CepikApiData'
path = "docs/CSVs/"
df = pd.read_csv('docs/voivodeship.csv')

original_date = '20100101'
current_date = datetime.now().strftime('%Y%m%d')
date_difference = int(current_date[:4])-2010

request_count = 0
MAX_REQUESTS = 100

for klucz,wartosc in zip(df['klucz-slownika'],df['wartosc-slownika']):
        for i in range(date_difference):
                k, match = 1, 2
                while k <= match:
                        if request_count >= MAX_REQUESTS:
                                log = "API rate limit reached. Waiting for a minute."
                                logging.info(log)
                                print(log)
                                time.sleep(60)
                                request_count = 0
                        try:
                                time.sleep(0.05)  # Ensure at most 20 requests per second
                                start_date = str(int(original_date[:4]) + i)+"0101"
                                next_date = str(int(start_date[:4])+1)+"1231"
                                params= {
                                        "wojewodztwo": str(klucz),
                                        "data-od": start_date,
                                        'data-do': next_date,
                                        "typ-daty": "1",
                                        "tylko-zarejestrowane": "true",
                                        "pokaz-wszystkie-pola": "false",
                                        "limit": "500",
                                        "page": str(k)
                                }
                                new_file_name=wartosc+" "+start_date+"-"+next_date+" "+str(k)+".csv"
                                print(wartosc+"/"+new_file_name)
                                if check_file(path+wartosc+"/",new_file_name):
                                        k += 1
                                        match += 1
                                        continue
                                print(new_file_name)
                                df, data = connect_and_dataload(api_link,params)
                                if "Error parsing JSON:" in df:
                                        df.to_csv("CSVs/")
                                last_link = data['links']['last']
                                match = re.search(r'page=(\d+)&typ-daty', last_link)
                                match = int(match.group(1))

                                df = pd.DataFrame(df)
                                df.columns = df.columns.str.replace('attributes.','', regex=True)
                                df.columns = df.columns.str.replace('-', '_', regex=True)
                                df = df.drop(columns=['links.self',
                                                      'typ',
                                                      'wariant',
                                                      'id',
                                                      'type',
                                                      'kategoria_pojazdu'
                                                      ])

                                df.to_csv(path+wartosc+"/"+new_file_name)
                                log = f"Request successful: Page {k} from max pages {match}, Date Range: {start_date} to {next_date}"
                                logging.info(log)
                                print(log)
                                k += 1
                                request_count += 1

                        except Exception as e:
                                logging.error(f"Failed to retrieve data: {e}")
                                print(f"Failed to retrieve data: {e}")
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
                                continue
                        
log = f"Vehicles file '{new_file_name}' has been created."
logging.info(log)
print(log)