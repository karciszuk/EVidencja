import requests
from requests.adapters import HTTPAdapter
import ssl

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', SSLAdapter())

base_url = "https://api.cepik.gov.pl/pojazdy"  # Replace with the actual URL
params = {
    'wojewodztwo': '30',
    'data-od': '20190101',
    'data-do': '20191231'
}

response = session.get(base_url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code} - {response.text}")