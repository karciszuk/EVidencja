import pandas as pd
from main import connect_and_dataload, to_database, to_csv, csv_name

api_link = "https://api.cepik.gov.pl/pojazdy"
params={
        "wojewodztwo": "30",
        "data-od": "20240101",
        'data-do': "20240131",
        "typ-daty": "1",
        "tylko-zarejestrowane": "true",
        "pokaz-wszystkie-pola": "false",
        "limit": "500",
        "page": "1"
         }
table = 'Statistics'

headers = connect_and_dataload(api_link,params=params)

#csvname = csv_name()

total_pages = headers.get('X-Total-Pages')
print(f"Total pages: {total_pages}")

#to_csv(df, csvname)