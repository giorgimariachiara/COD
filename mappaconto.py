import pandas as pd

# Carica i dati dal file CSV
df = pd.read_csv('uominimappa.csv')

# Conta il numero di uomini per regione
regione_counts = df['regione'].value_counts()

# Crea un DataFrame per le regioni italiane
regioni_italiane = pd.Series(range(1, 21), index=[
    'ABRUZZO', 'BASILICATA', 'CALABRIA', 'CAMPANIA', 'EMILIA-ROMAGNA',
    'FRIULI VENEZIA GIULIA', 'LAZIO', 'LIGURIA', 'LOMBARDIA', 'MARCHE',
    'MOLISE', 'PIEMONTE', 'PUGLIA', 'SARDEGNA', 'SICILIA', 'TOSCANA',
    'TRENTINO ALTO ADIGE', 'UMBRIA', 'VALLE D\'AOSTA', 'VENETO'
])

# Crea un DataFrame per i conteggi degli uomini per regione
uominimapconto_df = pd.DataFrame({'regione': regioni_italiane.index, 'count': regione_counts})

# Ordina il DataFrame in base alle regioni italiane
uominimapconto_df = uominimapconto_df.sort_values(by='regione')

# Riavvia l'indice del DataFrame
uominimapconto_df = uominimapconto_df.reset_index(drop=True)

# Salva il nuovo DataFrame in un nuovo file CSV 'uominimapconto.csv'
uominimapconto_df.to_csv('uominimapconto.csv', index=False)
