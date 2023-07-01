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

def create_contolegM_files():
    # Crea un dizionario per tenere traccia dei conteggi delle legislature
    legislatura_counts = {}

    # Ottieni tutti i file "legislatura_x_M.csv" nella directory corrente
    files = [f for f in os.listdir('.') if f.startswith('legislatura_') and f.endswith('_M.csv')]

    # Calcola i conteggi delle lauree per ogni legislatura
    for file in files:
        legislatura = file.split('_')[1]
        graduated_count, non_graduated_count = count_graduation(file)
        legislatura_counts[legislatura] = (graduated_count, non_graduated_count)

    # Crea un file contolegM.csv per ogni legislatura
    for legislatura, counts in legislatura_counts.items():
        output_file = f"contolegM_{legislatura}.csv"
        graduated_count, non_graduated_count = counts

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['graduated', 'non graduated'])
            writer.writerow([graduated_count, non_graduated_count])

# Chiamata alla funzione per creare i file "contolegM.csv" per ogni legislatura
create_contolegM_files()
