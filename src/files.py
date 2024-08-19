import pandas as pd
from main import connect_and_dataload, check_file
import requests
from requests.adapters import HTTPAdapter
import ssl
import pandas as pd

api_link = "https://api.cepik.gov.pl/pliki"
params={

}

class SSLAdapter(HTTPAdapter):
        def init_poolmanager(self, *args, **kwargs):
            ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            ctx.set_ciphers('DEFAULT@SECLEVEL=1')
            kwargs['ssl_context'] = ctx
            return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)
session = requests.Session()
session.mount('https://', SSLAdapter())

if check_file("","files.csv"):
    df = pd.read_csv('files.csv')
    for file_url in df["attributes.url-do-pliku"]:
        zip_file_response = requests.get(file_url)
        find = file_url.find("pojazdy")
        print(file_url[find:])
        with open("pojazdy_32_2022-04-17.zip", "wb") as file:
            file.write(zip_file_response.content)

else:
    df, data = connect_and_dataload(api_link,params=params)
    df.to_csv('files.csv')
    print(df.columns('attributes.url-do-pliku'))