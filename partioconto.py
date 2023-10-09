import pandas as pd

# Carica il file CSV in un DataFrame
df = pd.read_csv('partyallineamento.csv')

# Rinomina la colonna 'Allineamento Politico' senza spazi
df = df.rename(columns={'Allineamento Politico': 'AllineamentoPolitico'})

# Raggruppa il DataFrame per 'partito' e 'AllineamentoPolitico', quindi conta uomini e donne in ciascun gruppo
grouped = df.groupby(['partito', 'AllineamentoPolitico', 'gender'])['gender'].count().unstack(fill_value=0)

# Resetta l'indice per ottenere un DataFrame piatto
grouped = grouped.reset_index()

# Rinomina le colonne
grouped.columns.name = None
grouped = grouped.rename(columns={'male': 'numeroUomini', 'female': 'numeroDonne'})

# Salva il nuovo DataFrame in un nuovo file CSV
grouped.to_csv('conteggio_generi_per_partito.csv', index=False)
