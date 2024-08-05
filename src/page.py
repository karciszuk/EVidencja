import pandas as pd
from main import connect_and_dataload
import time
from datetime import datetime
import glob
import os
import re
import logging

api_link = "https://api.cepik.gov.pl/pojazdy"
table = 'CepikApiData'
path = "docs/CSVs/"
df = pd.read_csv('docs/voivodeship.csv')

original_date = '20100101'
current_date = datetime.now().strftime('%Y%m%d')
date_difference = int(current_date[:4])-2010
table = []

for klucz,wartosc in zip(df['klucz-slownika'],df['wartosc-slownika']):
        for i in range(date_difference):
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
                    "page": "1"
            }
            df, data = connect_and_dataload(api_link,params=params)

            last_link = data['links']['last']
            match = re.search(r'page=(\d+)&typ-daty', last_link)
            match = int(match.group(1))

            row = {wartosc: match}
            
            table.append(row)

print(table)