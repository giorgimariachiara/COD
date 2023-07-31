
"""
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



#aggiungo le legislature mergiando i due file: graduation.csv > graduatedMA.csv, graduationfemale.csv > graduatedFE



"""

import pandas as pd

# Leggi il file CSV
df = pd.read_csv('graduatedFE.csv')

# Mappa i valori della colonna "legislatura" con i corrispondenti valori desiderati
legislatura_mapping = {
    'legislatura costituente': 'costituente',
    'legislatura01': '1',
    'legislatura02': '2',
    'legislatura03': '3',
    'legislatura04': '4',
    'legislatura05': '5',
    'legislatura06': '6',
    'legislatura07': '7',
    'legislatura08': '8',
    'legislatura09': '9',
    'legislatura10': '10',
    'legislatura11': '11',
    'legislatura12': '12',
    'legislatura13': '13',
    'legislatura14': '14',
    'legislatura15': '15',
    'legislatura16': '16',
    'legislatura17': '17',
    'legislatura18': '18',
    'legislatura19': '19',
}

df['legislatura'] = df['legislatura'].map(legislatura_mapping)

# Salva il DataFrame aggiornato nel file CSV
df.to_csv('graduatedFEMALE.csv', index=False)


#colonna legislatura senza la parola 'legislatura' ma solo costituente e/o i numeri. graduationMA.csv >graduationMALE, graduationFE.csv > graduationFEMALE.csv


