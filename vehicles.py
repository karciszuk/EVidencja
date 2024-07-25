import pandas as pd
from main import connect_and_dataload, to_database, to_csv, csv_name
import time
from datetime import datetime

base_url = "https://api.cepik.gov.pl/pojazdy"
table = 'CepikApiData'
path = "CSVs/"
df = pd.read_csv('voivodeship.csv')

current_date = datetime.now().strftime('%Y%m%d')
date_difference = int(current_date[:4])-2010

original_date = '20100101'

for klucz,wartosc in zip(df['klucz-slownika'],df['wartosc-slownika']):
        for i in range(date_difference):
                start_date = str(int(original_date[:4]) + i)+original_date[4:]
                next_date = str(int(start_date[:4]) + 1)+"1231"
                params={
                        "wojewodztwo": klucz,
                        "data-od": start_date,
                        'data-do': current_date
                        }
                df = connect_and_dataload(base_url,params) 
                df.columns = df.columns.str.replace('attributes.','', regex=True)
                df.columns = df.columns.str.replace('-', '_', regex=True)
                df = df.drop(columns=['links.self'])

                to_csv(df,path+wartosc)

                time.sleep(2)

print("Vehicles .csv's created.")