import pandas as pd

# Original dictionary
data = {
    'id': '1220122406383331',
    'type': 'pojazdy',
    'attributes': {
        'marka': 'BMW',
        'kategoria-pojazdu': '0',
        'typ': '---',
        'model': 'X1',
        'wariant': '---',
        'rodzaj-pojazdu': 'SAMOCHÓD OSOBOWY',
        'pochodzenie-pojazdu': 'UŻYW. IMPORT INDYW',
        'rok-produkcji': 'FABRYCZNY',
        'data-pierwszej-rejestracji-w-kraju': '2019-01-01',
        'pojemnosc-skokowa-silnika': 1998.0,
        'masa-wlasna': 1580,
        'rodzaj-paliwa': 'BENZYNA',
        'wojewodztwo-kod': '30'
    },
    'links': {
        'self': 'https://api.cepik.gov.pl/pojazdy/1220122406383331'
    }
}

# Flatten the dictionary
flattened_data = {
    'id': data['id'],
    'type': data['type'],
    **data['attributes'],
    'link_self': data['links']['self']
}

# Convert to DataFrame
df = pd.DataFrame([flattened_data])

# Display the DataFrame
print(df)