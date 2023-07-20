import csv

input_file = 'ministrigender.csv'
output_file = 'ministero.csv'

ministri_set = set()

# Lettura del file CSV e aggiunta dei nomi dei ministri al set
with open(input_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        ministro = row['Ministro']
        ministri_set.add(ministro.lower())  # Aggiungi il nome del ministro in minuscolo al set

# Scrittura del file CSV con i nomi dei ministri senza duplicati
with open(output_file, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ministro'])
    for ministro in ministri_set:
        writer.writerow([ministro])

print("File 'ministero.csv' creato con successo.")
