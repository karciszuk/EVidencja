import pandas as pd
from ConnectAndDataload import connect_and_dataload

api_link = "https://api.cepik.gov.pl/slowniki/wojewodztwa"
params={}
table = 'Dictionary'

df, data = connect_and_dataload(api_link,params=params)

df = pd.json_normalize(data['data'])    

df_exploded = df.explode('attributes.dostepne-rekordy-slownika')
#dostepne_rekordy_df = pd.json_normalize(df_exploded)

#expanded_df = dostepne_rekordy_df['attributes.dostepne-rekordy-slownika'].apply(pd.Series)
#result_df = pd.concat([df.drop(columns=['attributes.dostepne-rekordy-slownika']), expanded_df], axis=1)

print(df_exploded)