import pandas as pd

# Carica i dati dal file CSV
df = pd.read_csv('graduatedFE.csv')

# Conta il numero di donne laureate per legislatura
count_df = df[df['graduated'] == 'yes'].groupby('legislatura').size().reset_index(name='graduated')
count_df['non graduated'] = df[df['graduated'] == 'no'].groupby('legislatura').size().values

# Salva i risultati in un nuovo file CSV
count_df.to_csv('laureaFE.csv', index=False)





#da graduatedFE il file delle donne con legislatura ho fatto il conto per avere i dati per google charts