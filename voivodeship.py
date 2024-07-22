import pandas as pd
from ConnectAndDataload import connect_and_dataload,to_csv

api_link = "https://api.cepik.gov.pl/slowniki/wojewodztwa"
params={}
table = 'Dictionary'

df, data = connect_and_dataload(api_link,params=params)
df = pd.json_normalize(data['data']) 
df_exploded = df.explode('attributes.dostepne-rekordy-slownika')
df_voivodeship = df_exploded['attributes.dostepne-rekordy-slownika']

# Check the type of an element in the exploded column
print(type(df_voivodeship.iloc[0]))  # Check the type of the first element

if isinstance(df_voivodeship.iloc[0], dict): # If the elements are dictionaries, you can iterate over them
    for item in df_voivodeship:
        for key, value in item.items():
            print(f"{key}: {value}")
else:
    print("Elements are not dictionaries")

df_voivodeship_table = pd.json_normalize(df_voivodeship.dropna().tolist()) # If needed, create a DataFrame from the list of dictionaries

to_csv(df_voivodeship_table)