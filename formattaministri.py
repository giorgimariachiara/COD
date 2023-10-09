import pandas as pd

# Carica il file CSV in un DataFrame
df = pd.read_csv('ministrilegislature.csv')

# Filtra le righe con genere "female"
df = df[df['gender'] == 'female']

# Rimuovi la colonna "gender"
df = df.drop(columns=['gender'])

# Estrai i numeri dalla colonna "legislatura" e crea una nuova colonna formattata
df['legislatura'] = df['legislatura'].str.extract('(\d+)').astype(int)

# Crea una nuova colonna "legislatura_formatted" con la formattazione desiderata
df['legislatura_formatted'] = 'legislatura ' + df['legislatura'].astype(str)

# Seleziona solo le colonne desiderate nel nuovo DataFrame
df = df[['Governo', 'Ministro', 'nome', 'cognome', 'legislatura_formatted']]

# Rinomina la colonna "legislatura_formatted" in "legislatura"
df = df.rename(columns={'legislatura_formatted': 'legislatura'})

# Salva il DataFrame risultante in un nuovo file CSV
df.to_csv('ministre.csv', index=False)
