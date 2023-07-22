
import pandas as pd

# Carica i file CSV
df1 = pd.read_csv('graduation.csv')
df2 = pd.read_csv('graduationfemale.csv')

# Unisci i due dataframe
merged_df = pd.concat([df1, df2], ignore_index=True)

# Salva il risultato in un nuovo file CSV
merged_df.to_csv('mergedgraduationtot.csv', index=False)

"""

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


#per creare file tot che è data csv. nel primo codice commentato unisco i due file senza legislature  nel secondo conto tutto 
"""