import pandas as pd

# Carica i dati dal primo file CSV
df1 = pd.read_csv('graduationfemale.csv')

# Carica i dati dal secondo file CSV
df2 = pd.read_csv('deputatiperlegislatura.csv')

# Effettua la fusione dei dati basata sulla colonna 'Persona'
merged_df = pd.merge(df1, df2, on='Persona')

# Seleziona solo le colonne desiderate
merged_df = merged_df[['Persona', 'legislatura', 'graduated']]

# Salva il risultato in un nuovo file CSV
merged_df.to_csv('graduatedFE.csv', index=False)
