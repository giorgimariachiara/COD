import pandas as pd

# Definisci l'ordine dei partiti desiderato
partiti_ordine = ['PARTITO COMUNISTA ITALIANO', 'DEMOCRAZIA PROLETARIA', 'PARTITO DI UNITÀ PROLETARIA PER IL COMUNISMO', 'PARTITO DELLA RIFONDAZIONE COMUNISTA - SINISTRA EUROPEA', 'SINISTRA INDIPENDENTE', 'PARTITO DEI COMUNISTI ITALIANI', 'SINISTRA ECOLOGIA LIBERTÀ', 'ROSA NEL PUGNO', 'PARTITO SOCIALISTA ITALIANO', 'L\'ULIVO', 'PARTITO DEMOCRATICO DELLA SINISTRA', 'ITALIA DEI VALORI', 'LIBERI E UGUALI', 'POPOLARI UDEUR', 'FORZA ITALIA', 'IL POPOLO DELLA LIBERTÀ', 'ALLEANZA NAZIONALE', 'FUTURO E LIBERTÀ PER L\'ITALIA', 'POPOLO E TERRITORIO', 'CENTRO DEMOCRATICO', 'PARTITO RADICALE', 'MISTO', 'PARTITO SOCIALISTA DEMOCRATICO ITALIANO', 'FEDERAZIONE DEI VERDI', 'PARTITO REPUBBLICANO ITALIANO', 'CENTRO CRISTIANO DEMOCRATICO', 'ITALIA VIVA', 'UNIONE DI CENTRO (2002)', 'CORAGGIO ITALIA', 'NUOVO CENTRODESTRA', 'RINNOVAMENTO ITALIANO', 'PARTITO SOCIALISTA ITALIANO DI UNITÀ PROLETARIA', 'DEMOCRAZIA CRISTIANA', 'PARTITO POPOLARE ITALIANO', 'DEMOCRAZIA NAZIONALE - COSTITUENTE DI DESTRA', 'LEGA NORD', 'PARTITO NAZIONALE MONARCHICO', 'MOVIMENTO SOCIALE ITALIANO - DESTRA NAZIONALE', 'FRONTE DELL\'UOMO QUALUNQUE']

# Carica il file CSV originale
df = pd.read_csv('partyspettro.csv')

# Crea il DataFrame per gli uomini
df_uomini = df[df['gender'] == 'male']
df_uomini = df_uomini.groupby(['partito']).agg({'Allineamento Politico': 'first'}).reset_index()
df_uomini['count'] = df_uomini.groupby('partito')['partito'].transform('count')
df_uomini = df_uomini[['partito', 'count', 'Allineamento Politico']]
df_uomini = df_uomini.drop_duplicates(subset=['partito'])
df_uomini = df_uomini.reindex(partiti_ordine)

# Crea il DataFrame per le donne
df_donne = df[df['gender'] == 'female']
df_donne = df_donne.groupby(['partito']).agg({'Allineamento Politico': 'first'}).reset_index()
df_donne['count'] = df_donne.groupby('partito')['partito'].transform('count')
df_donne = df_donne[['partito', 'count', 'Allineamento Politico']]
df_donne = df_donne.drop_duplicates(subset=['partito'])
df_donne = df_donne.reindex(partiti_ordine)

# Salva i DataFrame in due file CSV separati
df_uomini.to_csv('partiti_uomini.csv', index=False)
df_donne.to_csv('partiti_donne.csv', index=False)
