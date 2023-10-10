"""
++++++++++ WHAT: da graduationfemale.csv (file senza lrgislature) ho creato graduatedFE.csv che ha le legislature



+++++++++++++++++++


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

 """
"""

import pandas as pd

# Leggi i file CSV
df_FE = pd.read_csv('graduatedFE.csv')
df_MA = pd.read_csv('graduatedMA.csv')

# Mappa degli URL alle numerazioni delle legislature
legislatura_mapping = {
    'http://dati.camera.it/ocd/legislatura.rdf/costituente': 'costituente',
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_01': 1,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_02': 2,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_03': 3,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_04': 4,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_05': 5,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_06': 6,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_07': 7,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_08': 8,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_09': 9,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_10': 10,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_11': 11,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_12': 12,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_13': 13,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_14': 14,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_15': 15,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_16': 16,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_17': 17,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_18': 18,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_19': 19
}

# Applica la mappatura alle colonne "legislatura" dei DataFrame
df_FE['legislatura'] = df_FE['legislatura'].map(legislatura_mapping)
df_MA['legislatura'] = df_MA['legislatura'].map(legislatura_mapping)

# Salva i DataFrame risultanti in nuovi file CSV se necessario
df_FE.to_csv('graduatedFEMALE.csv', index=False)
df_MA.to_csv('graduatedMALE.csv', index=False)


"""
"""
import pandas as pd

# Leggi i file CSV
df_FEMALE = pd.read_csv('graduatedFEMALE.csv')
df_MALE = pd.read_csv('graduatedMALE.csv')

# Crea una funzione per contare le laureate e non laureate per legislatura
def count_graduates_by_legislature(df):
    count = df.groupby(['legislatura', 'graduated']).size().unstack(fill_value=0)
    count['Total'] = count.sum(axis=1)
    return count

# Conta le laureate e non laureate per legislatura nel DataFrame femminile
female_counts = count_graduates_by_legislature(df_FEMALE)

# Conta le laureate e non laureate per legislatura nel DataFrame maschile
male_counts = count_graduates_by_legislature(df_MALE)

# Unisci i conteggi femminili e maschili in un unico DataFrame
result = pd.concat([female_counts, male_counts], axis=1, keys=['FEMALE', 'MALE'])
result.columns = result.columns.map('_'.join)

# Resetta gli indici per ottenere una colonna 'legislatura'
result.reset_index(inplace=True)

# Salva il DataFrame risultante in un nuovo file CSV
result.to_csv('graduatedCount.csv', index=False)


"""
"""
import pandas as pd

# Leggi il file CSV con i conteggi
df = pd.read_csv('graduatedCount.csv')

# Calcola e arrotonda le percentuali per legislatura e genere
df['FEMALE_no_percent'] = (df['FEMALE_no'] / df['FEMALE_Total'] * 100).round().astype(int)
df['FEMALE_yes_percent'] = (df['FEMALE_yes'] / df['FEMALE_Total'] * 100).round().astype(int)
df['MALE_no_percent'] = (df['MALE_no'] / df['MALE_Total'] * 100).round().astype(int)
df['MALE_yes_percent'] = (df['MALE_yes'] / df['MALE_Total'] * 100).round().astype(int)

# Seleziona solo le colonne di percentuale
percentages_df = df[['legislatura', 'FEMALE_no_percent', 'FEMALE_yes_percent', 'MALE_no_percent', 'MALE_yes_percent']]

# Salva il DataFrame con le percentuali arrotondate in un nuovo file CSV
percentages_df.to_csv('graduatedPercentages.csv', index=False)


"""

import pandas as pd

# Leggi il file CSV
df = pd.read_csv('graduatedPercentages.csv')

# Filtra solo le righe relative agli uomini
df_men = df[df['legislatura'] != 'costituente']

# Filtra solo le righe relative alle donne
df_women = df[df['legislatura'] == 'costituente']

# Calcola la media, la moda e i numeri più bassi per gli uomini
mean_men = df_men['MALE_yes_percent'].mean()
mode_men = df_men['MALE_yes_percent'].mode().iloc[0]
min_men = df_men['MALE_yes_percent'].min()

# Calcola la media, la moda e i numeri più bassi per le donne
mean_women = df_women['FEMALE_yes_percent'].mean()
mode_women = df_women['FEMALE_yes_percent'].mode().iloc[0]
min_women = df_women['FEMALE_yes_percent'].min()

# Stampa i risultati per gli uomini
print("Media delle percentuali di rappresentanti maschili laureati:", mean_men)
print("Moda delle percentuali di rappresentanti maschili laureati:", mode_men)
print("Percentuale più bassa di rappresentanti maschili laureati:", min_men)

# Stampa i risultati per le donne
print("\nMedia delle percentuali di rappresentanti femminili laureate:", mean_women)
print("Moda delle percentuali di rappresentanti femminili laureate:", mode_women)
print("Percentuale più bassa di rappresentanti femminili laureate:", min_women)

# Trova le legislature con la percentuale più bassa di rappresentanti maschili laureati
min_legislature_men = df_men[df_men['MALE_yes_percent'] == min_men]['legislatura'].tolist()
print("\nLegislature con la percentuale più bassa di rappresentanti maschili laureati:", min_legislature_men)

# Trova le legislature con la percentuale più alta di rappresentanti maschili laureati
max_men = df_men['MALE_yes_percent'].max()
max_legislature_men = df_men[df_men['MALE_yes_percent'] == max_men]['legislatura'].tolist()
print("Legislature con la percentuale più alta di rappresentanti maschili laureati:", max_legislature_men)

# Trova le legislature con la percentuale più bassa di rappresentanti femminili laureate
min_legislature_women = df_women[df_women['FEMALE_yes_percent'] == min_women]['legislatura'].tolist()
print("\nLegislature con la percentuale più bassa di rappresentanti femminili laureate:", min_legislature_women)

# Trova le legislature con la percentuale più alta di rappresentanti femminili laureate
max_women = df_women['FEMALE_yes_percent'].max()
max_legislature_women = df_women[df_women['FEMALE_yes_percent'] == max_women]['legislatura'].tolist()
print("Legislature con la percentuale più alta di rappresentanti femminili laureate:", max_legislature_women)


""" 
Media delle percentuali di rappresentanti maschili laureati: 67
Moda delle percentuali di rappresentanti maschili laureati: 69
Percentuale più bassa di rappresentanti maschili laureati: 63

Media delle percentuali di rappresentanti femminili laureate: 60.0
Moda delle percentuali di rappresentanti femminili laureate: 60
Percentuale più bassa di rappresentanti femminili laureate: 60

Legislature con la percentuale più bassa di rappresentanti maschili laureati: ['16', '18']
Legislature con la percentuale più alta di rappresentanti maschili laureati: ['1']

Legislature con la percentuale più bassa di rappresentanti femminili laureate: ['costituente']
Legislature con la percentuale più alta di rappresentanti femminili laureate: ['costituente']
""" 



""" 
+++++++++++ WHAT: da graduatedFE il file delle donne con legislatura ho fatto il conto per avere i dati per google charts ++++++++++++++++


import pandas as pd

# Carica i dati dal file CSV
df = pd.read_csv('graduatedFE.csv')

# Conta il numero di donne laureate per legislatura
count_df = df[df['graduated'] == 'yes'].groupby('legislatura').size().reset_index(name='graduated')
count_df['non graduated'] = df[df['graduated'] == 'no'].groupby('legislatura').size().values

# Salva i risultati in un nuovo file CSV
count_df.to_csv('laureaFE.csv', index=False)


"""




"""

+++++++++WHAT: per creare file tot che è data csv. nel primo codice unisco i due file senza legislature,  nel secondo conto tutto +++++++++

import pandas as pd

# Carica i file CSV
df1 = pd.read_csv('graduation.csv')
df2 = pd.read_csv('graduationfemale.csv')

# Unisci i due dataframe
merged_df = pd.concat([df1, df2], ignore_index=True)

# Salva il risultato in un nuovo file CSV
merged_df.to_csv('mergedgraduationtot.csv', index=False)



import csv

# Leggi il file CSV originale
with open('mergedgraduationtot.csv', mode='r') as file:
    reader = csv.reader(file)
    data = list(reader)

# Rimuovi l'intestazione dal file originale
header = data[0]
data = data[1:]

# Calcola i totali per genere
gender_counts = {}
graduated_counts = {}
non_graduated_counts = {}

for row in data:
    gender = row[1]
    graduated = row[2]

    gender_counts[gender] = gender_counts.get(gender, 0) + 1
    if graduated == 'yes':
        graduated_counts[gender] = graduated_counts.get(gender, 0) + 1

# Crea i dati finali per Google Charts
final_data = [['Gender', 'Graduated', 'Non-Graduated', 'Tot']]

for gender in gender_counts.keys():
    graduated = graduated_counts.get(gender, 0)
    non_graduated = gender_counts[gender] - graduated
    total = gender_counts[gender]
    final_data.append([gender, graduated, non_graduated, total])

# Scrivi i dati finali nel file CSV per Google Charts
with open('gradcountot.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(final_data)

print("File CSV creato correttamente per Google Charts.")


"""



"""

import pandas as pd

# Carica i dati dal file CSV
df = pd.read_csv('OK3graduationFEMALE.csv')

# Conta i valori NaN nella colonna 'graduated'
nan_count = df['graduated'].isna().sum()

# Stampa il numero di valori NaN
print("Numero di valori NaN nella colonna 'graduated':", nan_count)

"""





"""

+++++WHAT: prende i grdaduationMA.csv e graduationFE.csv per sistemare la formattazione delle legislature.  ++++++++

"""

"""
import pandas as pd

# Read the CSV dataset using Pandas
data = pd.read_csv('graduatedFE.csv')

# Define a function to format the legislature name
def format_legislature_name(legislature):
    if legislature.lower() == 'legislaturacostituente':
        return 'Legislatura Costituente'
    else:
        num_part = ''.join(filter(str.isdigit, legislature))
        num_part = num_part.lstrip('0')
        return 'Legislatura ' + num_part

# Apply the function to format the legislature name and update the 'legislatura' column
data['legislatura'] = data['legislatura'].apply(format_legislature_name)

# Save the updated DataFrame to a new CSV file with the correct name
data.to_csv('graduatedFEMALE.csv', index=False)

# Print a message indicating the process is complete
print("CSV file with modified legislature names has been created.")
"""