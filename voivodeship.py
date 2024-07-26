import pandas as pd
from main import connect_and_dataload, to_database, to_csv, csv_name

api_link = "https://api.cepik.gov.pl/slowniki/wojewodztwa"
params={}
table = 'Dictionary'

df = connect_and_dataload(api_link,params=params)
df_exploded = df.explode('attributes.dostepne-rekordy-slownika')
df_voivodeship = df_exploded['attributes.dostepne-rekordy-slownika']

df_voivodeship_table = pd.json_normalize(df_voivodeship.dropna().tolist()) # If needed, create a DataFrame from the list of dictionaries

csvname = csv_name()

to_csv(df_voivodeship_table, csvname)