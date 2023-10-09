import pandas as pd

# Leggi il file CSV in un DataFrame
df = pd.read_csv('partyallineamento.csv')

# Raggruppa i dati per partito e allineamento politico e calcola il conteggio di uomini e donne in ciascun gruppo
grouped = df.groupby(['partito', 'AllineamentoPolitico']).gender.value_counts().unstack(fill_value=0).reset_index()

# Rinomina le colonne
grouped.columns.name = None  # Rimuovi il nome delle colonne
grouped.columns = ['partito', 'allineamentoPolitico', 'numeroDonne', 'numeroUomini']

# Salva il DataFrame risultante in un nuovo file CSV
grouped.to_csv('output.csv', index=False)
