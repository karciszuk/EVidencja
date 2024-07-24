import pandas as pd
from main import connect_and_dataload, to_database, to_csv, csv_name

api_link = "https://api.cepik.gov.pl/pojazdy"
table = 'CepikApiData'

df = pd.read_csv('voivodeship.csv')

for klucz,wartosc in zip(df['klucz-slownika'],df['wartosc-slownika']):
        voivodeship = klucz
        params={
                "wojewodztwo": 30,
                "data-od": "20100101"
                }
        df, data = connect_and_dataload(api_link,params)
        df = pd.json_normalize(data['data'])    
        df.columns = df.columns.str.replace('attributes.','', regex=True)
        df.columns = df.columns.str.replace('-', '_', regex=True)
        df = df.drop(columns=['links.self'])
        to_csv(df,wartosc)