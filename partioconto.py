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
grouped.to_csv('conteggio_generi_per_partito.csv', index=False)
"""

"""
import pandas as pd

# Carica il file CSV in un DataFrame
df = pd.read_csv('conteggio_generi_per_partito.csv')

# Calcola la colonna 'PercentualeDonne' e arrotonda al numero intero
df['PercentualeDonne'] = ((df['numeroDonne'] / (df['numeroDonne'] + df['numeroUomini'])) * 100).round().astype(int)

# Calcola la colonna 'PercentualeUomini' e arrotonda al numero intero
df['PercentualeUomini'] = ((df['numeroUomini'] / (df['numeroDonne'] + df['numeroUomini'])) * 100).round().astype(int)

# Salva il DataFrame aggiornato in un nuovo file CSV
df.to_csv('percentagePartiti.csv', index=False)
"""


import pandas as pd

# Carica il file CSV in un DataFrame
df = pd.read_csv('percentagePartiti.csv.csv')

# Raggruppa il DataFrame per 'AllineamentoPolitico' e calcola la media delle percentuali di donne
media_percentuali_donne = df.groupby('AllineamentoPolitico')['PercentualeDonne'].mean()

# Trova l'allineamento politico con la percentuale di donne più alta
allineamento_con_più_donne = media_percentuali_donne.idxmax()
percentuale_più_donne = media_percentuali_donne.max()

# Trova l'allineamento politico con la percentuale di donne più bassa
allineamento_con_meno_donne = media_percentuali_donne.idxmin()
percentuale_meno_donne = media_percentuali_donne.min()

print(f"Allineamento politico con più donne: {allineamento_con_più_donne} ({percentuale_più_donne:.2f}%)")
print(f"Allineamento politico con meno donne: {allineamento_con_meno_donne} ({percentuale_meno_donne:.2f}%)")
