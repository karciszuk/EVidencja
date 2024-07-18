import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl
import pandas as pd
from pandas import json_normalize
import sqlalchemy as sa
from conxn import coxn
import json
from datetime import datetime

session.get("https://api.cepik.gov.pl/pojazdy", params={
    "wojewodztwo": "30",
    "data-od": "20100101"