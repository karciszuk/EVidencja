import pandas as pd
import requests
from main import connect_and_dataload, to_database, to_csv, csv_name
import re

api_link = "https://api.cepik.gov.pl/pojazdy"
params={
        "wojewodztwo": "30",
        "data-od": "20200101",
        "data-do": "20211231",
        "typ-daty": "1",
        "tylko-zarejestrowane": "true",
        "pokaz-wszystkie-pola": "false",
        "limit": "500"
        }

df,data = connect_and_dataload(api_link,params=params)

print(df.columns)

last_link = data['links']['last']
match = re.search(r'page=(\d+)&typ-daty', last_link)
if match:
    print(match.group(1))
else:
    print("Pattern not found")