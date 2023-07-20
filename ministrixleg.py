"""

import pandas as pd

# Leggi il file CSV con i dati
df = pd.read_csv('ministrixleF.csv')

# Rimuovi le colonne "nome" e "cognome"
df = df.drop(['nome', 'cognome'], axis=1)

# Salva il dataframe in un nuovo file CSV
df.to_csv('ministriFGL.csv', index=False)
"""

import pandas as pd

# Carica il file CSV originale
file_input = "ministrixleF.csv"
dataframe = pd.read_csv(file_input)

# Elimina la colonna "gender"
dataframe = dataframe.drop(columns=["gender"])

# Salva il nuovo dataframe in un nuovo file CSV chiamato "ministre.csv"
file_output = "ministre.csv"
dataframe.to_csv(file_output, index=False)

print(f"File {file_output} creato con successo senza la colonna 'gender'.")
