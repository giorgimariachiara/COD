import csv

input_file = 'partyspettro.csv'  # Nome del file CSV di input
output_file = 'output.csv'  # Nome del file CSV di output

# Dizionario per tenere traccia del conteggio di uomini e donne per partito
parties = {}

# Apri il file di input in modalità lettura
with open(input_file, 'r') as file:
    reader = csv.reader(file)
    header = next(reader)  # Leggi l'intestazione del file

    # Indici delle colonne nel file di input
    party_index = header.index('partito')
    gender_index = header.index('gender')
    alignment_index = header.index('Allineamento Politico')

    # Elabora le righe del file di input
    for row in reader:
        party = row[party_index]
        gender = row[gender_index]
        alignment = row[alignment_index]

        # Controlla se il partito esiste già nel dizionario
        if party in parties:
            if gender == 'Male':
                parties[party]['male'] += 1
            elif gender == 'Female':
                parties[party]['female'] += 1
        else:
            # Crea un nuovo dizionario per il partito
            parties[party] = {'male': 0, 'female': 0}

            if gender == 'Male':
                parties[party]['male'] = 1
            elif gender == 'Female':
                parties[party]['female'] = 1

        # Aggiungi l'allineamento politico al dizionario del partito
        parties[party]['alignment'] = alignment

# Apri il file di output in modalità scrittura
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)

    # Scrivi l'intestazione del file di output
    writer.writerow(['partito', 'male', 'female', 'allineamento politico'])

    # Scrivi i dati per ogni partito nel file di output
    for party, data in parties.items():
        writer.writerow([party, data['male'], data['female'], data['alignment']])

print("Elaborazione completata. Il nuovo file CSV è stato creato.")
