import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from main import connect_and_dataload, check_file
import ssl
from zipfile import ZipFile, BadZipFile
from io import BytesIO

api_link = "https://api.cepik.gov.pl/pliki"
params = {}

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', SSLAdapter())

def download_and_extract_zip(url):
    response = session.get(url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        chunks = []
        
        # Download in chunks and update progress
        for chunk in response.iter_content(1024 * 1024):  # 1MB chunks
            if chunk:  # filter out keep-alive new chunks
                chunks.append(chunk)
                downloaded_size += len(chunk)
                print(f"Downloaded {downloaded_size / 1024 / 1024:.2f} MB of {total_size / 1024 / 1024:.2f} MB", end='\r')

        # Combine all chunks
        file_content = BytesIO(b''.join(chunks))

        try:
            with ZipFile(file_content) as zip_file:
                zip_file.extractall("docs/bulk/")
                print(f"\nFiles extracted successfully from {url}")
        except BadZipFile:
            print(f"\nFailed to extract file from {url}: Not a ZIP file")
    else:
        print(f"\nFailed to download file from {url}: HTTP {response.status_code}")

if check_file("docs/", "files.csv"):
    df = pd.read_csv('files.csv')
    for file_url in df["attributes.url-do-pliku"]:
        print
        if check_file("docs/bulk/", file_url[35:len(file_url)-3]+"csv"):
            print(f"{file_url} already downloaded")
        else:
            download_and_extract_zip(file_url)
else:
    df, data = connect_and_dataload(api_link, params=params)
    df.to_csv('files.csv')
    print("New files.csv created.")