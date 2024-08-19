import pandas as pd
from main import connect_and_dataload, check_file
from datetime import datetime
import re
import logging

# Configure logging
logging.basicConfig(
        filename='docs/api_requests.log', 
        level=logging.INFO, 
        format='%(asctime)s %(levelname)s:%(message)s')

api_link = "https://api.cepik.gov.pl/pojazdy"
table = 'CepikApiData'
path = "docs/CSVs/"
df = pd.read_csv('docs/voivodeship.csv')

original_date = '20100101'
current_date = datetime.now().strftime('%Y%m%d')
date_difference = int(current_date[:4])-2010

for klucz,wartosc in zip(df['klucz-slownika'],df['wartosc-slownika']):
        for i in range(date_difference):
                k, match = 1, 2
                while k <= match:
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
                        
                        k += 1

log = f"Vehicles file '{new_file_name}' has been created."
logging.info(log)
print(log)