import pandas as pd

# Carica i dati dal file CSV
df = pd.read_csv('graduationfemale.csv')

# Conta i valori NaN nella colonna 'graduated'
nan_count = df['graduated'].isna().sum()

# Stampa il numero di valori NaN
print("Numero di valori NaN nella colonna 'graduated':", nan_count)
