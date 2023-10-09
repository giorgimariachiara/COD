"""
++++++++++ WHAT: da graduationfemale.csv (file senza lrgislature) ho creato graduatedFE.csv che ha le legislature



+++++++++++++++++++
 """

import pandas as pd

# Carica i dati dal primo file CSV
df1 = pd.read_csv('OK3graduation.csv')

# Carica i dati dal secondo file CSV
df2 = pd.read_csv('deputatiperlegislatura.csv')

# Effettua la fusione dei dati basata sulla colonna 'Persona'
merged_df = pd.merge(df1, df2, on='Persona')

# Seleziona solo le colonne desiderate
merged_df = merged_df[['Persona', 'legislatura', 'graduated']]

# Salva il risultato in un nuovo file CSV
merged_df.to_csv('OK3graduatedMA.csv', index=False)







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





import pandas as pd

# Carica i dati dal file CSV
df = pd.read_csv('OK3graduationFEMALE.csv')

# Conta i valori NaN nella colonna 'graduated'
nan_count = df['graduated'].isna().sum()

# Stampa il numero di valori NaN
print("Numero di valori NaN nella colonna 'graduated':", nan_count)







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