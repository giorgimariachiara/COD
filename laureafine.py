import csv
import os

def count_graduation(file):
    graduated_count = 0
    non_graduated_count = 0

    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Salta l'intestazione
        for row in reader:
            graduated = row[1]
            if graduated == 'yes':
                graduated_count += 1
            else:
                non_graduated_count += 1

    return graduated_count, non_graduated_count

def create_laurea_file():
    # Crea un dizionario per tenere traccia dei conteggi delle legislature
    legislatura_counts = {}

    # Ottieni tutti i file "contolegM_x.csv" nella directory corrente
    files = [f for f in os.listdir('.') if f.startswith('contolegM_') and f.endswith('.csv')]

    # Calcola i conteggi delle lauree per ogni legislatura
    for file in files:
        legislatura = file.split('_')[1].split('.')[0]
        if legislatura == 'costituente':
            legislatura_num = 0
        else:
            legislatura_num = int(legislatura)
        with open(file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Salta l'intestazione
            counts = next(reader)
            graduated_count = int(counts[0])
            non_graduated_count = int(counts[1])
            legislatura_counts[legislatura_num] = (graduated_count, non_graduated_count)

    # Crea il file laurea.csv che riunisce i conteggi per legislatura in ordine
    with open('laurea.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['legislatura', 'graduated', 'non graduated'])
        for legislatura in range(0, 20):  # Da costituente a legislatura 19
            counts = legislatura_counts.get(legislatura, (0, 0))
            graduated_count, non_graduated_count = counts
            writer.writerow([legislatura, graduated_count, non_graduated_count])

# Chiamata alla funzione per creare il file "laurea.csv"
create_laurea_file()
