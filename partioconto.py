"""
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
grouped.to_csv('countParty.csv', index=False)
"""
"""

import pandas as pd

# Carica il file CSV in un DataFrame
df = pd.read_csv('countParty.csv')

# Calcola la colonna 'PercentualeDonne' e arrotonda al numero intero
df['PercentualeDonne'] = ((df['numeroDonne'] / (df['numeroDonne'] + df['numeroUomini'])) * 100).round().astype(int)

# Calcola la colonna 'PercentualeUomini' e arrotonda al numero intero
df['PercentualeUomini'] = ((df['numeroUomini'] / (df['numeroDonne'] + df['numeroUomini'])) * 100).round().astype(int)

# Salva il DataFrame aggiornato in un nuovo file CSV
df.to_csv('percParty.csv', index=False)

"""
"""
import pandas as pd

# Carica il file CSV in un DataFrame
df = pd.read_csv('percParty.csv')

# Calcola la media delle percentuali di donne per ciascun AllineamentoPolitico
media_percentuali_donne = df.groupby('AllineamentoPolitico')['PercentualeDonne'].mean().reset_index()

# Ordina il DataFrame in base alle percentuali di donne in ordine decrescente
classifica_orientamenti = media_percentuali_donne.sort_values(by='PercentualeDonne', ascending=False)

# Stampa la classifica
print("Classifica degli orientamenti politici da più donne a meno donne:")
print(classifica_orientamenti)

  AllineamentoPolitico  PercentualeDonne
7       trasversalismo         41.000000
6             sinistra         20.666667
1        centro-destra         18.400000
5     estrema sinistra         16.200000
2      centro-sinistra         14.200000
0               centro         11.714286
3               destra          9.777778
4       estrema destra          3.000000


"""
"""
import pandas as pd

# Carica il file CSV in un DataFrame
df = pd.read_csv('countParty.csv')

# Calcola la colonna 'PercentualeDonne' e arrotonda al numero intero
df['PercentualeDonne'] = ((df['numeroDonne'] / (df['numeroDonne'] + df['numeroUomini'])) * 100).round().astype(int)

# Ordina il DataFrame in base alla percentuale di donne in ordine decrescente
df_sorted = df.sort_values(by='PercentualeDonne', ascending=False)

# Prendi i primi 5 partiti con la percentuale più alta di donne
top_5_partiti_con_donne = df_sorted.head(5)

# Stampa i risultati
print("I 5 partiti con la percentuale più alta di donne sono:")
print(top_5_partiti_con_donne)
"""
"""utput 
I 5 partiti con la percentuale più alta di donne sono:
                partito  ... PercentualeDonne
20   MOVIMENTO 5 STELLE  ...               41
16          ITALIA VIVA  ...               39
4       CORAGGIO ITALIA  ...               35
27  PARTITO DEMOCRATICO  ...               34
3    CENTRO DEMOCRATICO  ...               30

"""