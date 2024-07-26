import pandas as pd
from main import connect_and_dataload, to_database, to_csv, csv_name
import time
from datetime import datetime
import glob
import os
import calendar

def check_file(path,name):
        files = glob.glob(os.path.join(path, name))
        return files

base_url = "https://api.cepik.gov.pl/pojazdy"
table = 'CepikApiData'
path = "CSVs/"
df = pd.read_csv('voivodeship.csv')

current_date = datetime.now().strftime('%Y%m%d')
date_difference = int(current_date[:4])-2010


for klucz,wartosc in zip(df['klucz-slownika'],df['wartosc-slownika']):
        original_date = '20100101'
        for i in range(date_difference):
                for l in range(1,12):
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
                                "page": "5"
                                }
                        new_file_name=wartosc+" "+start_date+"-"+next_date+".csv"
                        print(new_file_name)
                        files = check_file(path,new_file_name)   
                        print(files)
                        if files:
                                continue
                        df = connect_and_dataload(base_url,params) 
                        df.columns = df.columns.str.replace('attributes.','', regex=True)
                        df.columns = df.columns.str.replace('-', '_', regex=True)
                        df = df.drop(columns=['links.self'])

                        to_csv(df,path+new_file_name)

                        time.sleep(2)

print("Vehicles .csv's created.")