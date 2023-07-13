import pandas as pd

# Leggi il file CSV con i dati
df = pd.read_csv('ministrixleF.csv')

# Rimuovi le colonne "nome" e "cognome"
df = df.drop(['nome', 'cognome'], axis=1)

# Salva il dataframe in un nuovo file CSV
df.to_csv('ministriFGL.csv', index=False)
