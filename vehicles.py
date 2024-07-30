import pandas as pd
from main import connect_and_dataload, to_database, to_csv, csv_name
import time
from datetime import datetime
import glob
import os
import calendar
import re

def check_file(path,name):
        files = glob.glob(os.path.join(path, name))
        return files

api_link = "https://api.cepik.gov.pl/pojazdy"
table = 'CepikApiData'
path = "CSVs/"
df = pd.read_csv('voivodeship.csv')

current_date = datetime.now().strftime('%Y%m%d')
date_difference = int(current_date[:4])-2010

for klucz,wartosc in zip(df['klucz-slownika'],df['wartosc-slownika']):
        original_date = '20100101'
        for i in range(date_difference):
                for l in range(1,12):
                        k = 1
                        match = 1
                        while k <= match:
                                if l < 10:
                                        month = "0"+str(l)
                                else:
                                        month = str(l)
                                start_date = str(int(original_date[:4]) + i)+month+"01"
                                last_day = str(calendar.monthrange(int(start_date[:4]), int(month))[1])
                                next_date = str(int(start_date[:4]))+month+last_day
                                params={
                                        "wojewodztwo": str(klucz),
                                        "data-od": start_date,
                                        'data-do': next_date,
                                        "typ-daty": "1",
                                        "tylko-zarejestrowane": "true",
                                        "pokaz-wszystkie-pola": "false",
                                        "limit": "500",
                                        "page": str(k)
                                        }
                                new_file_name=wartosc+" "+start_date+"-"+next_date+".csv"
                                files = check_file(path,new_file_name)   
                                if files:
                                        continue
                                df, data = connect_and_dataload(api_link,params) 
                                last_link = data['links']['last']
                                match = int(re.search(r'page=(\d+)&typ-daty', last_link))
                                if match:
                                        print(match.group(1))
                                else:
                                        print("Pattern not found")
                                df = pd.DataFrame(df)
                                df.columns = df.columns.str.replace('attributes.','', regex=True)
                                df.columns = df.columns.str.replace('-', '_', regex=True)
                                df = df.drop(columns=['links.self'])

                                to_csv(df,path+new_file_name)

                                time.sleep(0.7)

                                k += 1

print(f"Vehicles file '{new_file_name}' has been created.")