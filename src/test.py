import pandas as pd

df = pd.read_csv('voivodeship.csv')
for klucz,wartosc in zip(df['klucz-slownika'],df['wartosc-slownika']):
        for i in range(5):
                k = 1
                match = 2
                while k <= match:
                        print("woj: "+str(klucz)+" ", end=' ')
                        print("itr: "+str(k)+" ", end=' ')
                        match = 5
                        print("new match: "+str(match)+" ", end=' ')
                        k += 1
                        print("new itr: "+str(k))