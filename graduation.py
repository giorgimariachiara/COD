import csv
import os
import math

def count_graduation(file):
    graduated_count = 0
    non_graduated_count = 0
    nan_count = 0

    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Salta l'intestazione
        for row in reader:
            graduated = row[1]
            if graduated == 'yes':
                graduated_count += 1
            elif graduated == 'no':
                non_graduated_count += 1
            elif isinstance(graduated, str) and graduated.lower() == 'nan':
                nan_count += 1

    return graduated_count, non_graduated_count, nan_count

def create_contolegF_files():
    # Crea un dizionario per tenere traccia dei conteggi delle legislature
    legislatura_counts = {}

    # Ottieni tutti i file "legislatura_x_M.csv" nella directory corrente
    files = [f for f in os.listdir('.') if f.startswith('legislatura_') and f.endswith('_F.csv')]

    # Calcola i conteggi delle lauree per ogni legislatura
    for file in files:
        legislatura = file.split('_')[1]
        graduated_count, non_graduated_count, nan_count = count_graduation(file)
        legislatura_counts[legislatura] = (graduated_count, non_graduated_count, nan_count)

    # Crea un file contolegM.csv per ogni legislatura
    for legislatura, counts in legislatura_counts.items():
        output_file = f"contolegF_{legislatura}.csv"
        graduated_count, non_graduated_count, nan_count = counts

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['graduated', 'non graduated', 'NaN'])
            writer.writerow([graduated_count, non_graduated_count, nan_count])

# Chiamata alla funzione per creare i file "contolegM.csv" per ogni legislatura
create_contolegF_files()
