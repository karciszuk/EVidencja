import os
from pathlib import Path
import os
import inspect
import pandas as pd

def list_csv_files(folder_path):
    files = os.listdir(folder_path) # List all files in the directory
    csv_files = [file for file in files if file.endswith('.csv')] # Filter and list CSV files
    return csv_files

csv_dir = "CSVs/" # Specify the path to your folder here
csv_list = []
df_list = []
    
csv_files = list_csv_files(csv_dir)

df = pd.read_csv('voivodeship.csv')
n = 0
i = 1
l = 0
temp_list = []

for wartosc in df['wartosc-slownika']:
    df_list = []
    for filename in csv_files:
        id = filename.find(" ")
        if str(wartosc) == str(filename[:id]):
            temp_list.append(wartosc)
            file_path = os.path.join(csv_dir, filename)
            df = pd.read_csv(file_path)
            df_list.append(df)
    if wartosc in temp_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        combined_df.to_csv("CombinedCSVs/"+wartosc+'.csv', index=False)