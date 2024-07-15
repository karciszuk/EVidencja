import pyodbc 
import sqlalchemy as sa 
from sqlalchemy import create_engine 
import urllib 

conn = urllib.parse.quote_plus( 
    'Data Source Name=qrice;' 
    'Driver={ODBC Driver 17 for SQL Server};' 
    'Server=QRICE;' 
    'Database=cepik;' 
    'Trusted_connection=yes;' 
    
) 
coxn = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn)) 