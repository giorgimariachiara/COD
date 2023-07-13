import csv

def count_female_per_party(input_file, output_file):
    party_data = {}  # Dizionario per memorizzare i conteggi delle donne per partito

    # Apertura del file di input in modalità di lettura
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Salta l'intestazione del file

        # Iterazione sulle righe del file di input
        for row in reader:
            party = row[0]
            gender = row[1]

            # Conta solo le donne e ignora le informazioni sugli uomini
            if gender.lower() == 'female':
                # Aggiungi il partito al dizionario se non esiste ancora
                if party not in party_data:
                    party_data[party] = {
                        'count': 0,
                        'alignment': row[2]
                    }

                # Incrementa il conteggio delle donne per il partito corrente
                party_data[party]['count'] += 1

    # Scrittura dei dati nel file di output
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['partito', 'count', 'allineamento politico'])  # Intestazione del file

        # Iterazione sui dati del dizionario per scrivere le righe nel file di output
        for party, data in party_data.items():
            writer.writerow([party, data['count'], data['alignment']])

    print("Elaborazione completata. Il file 'donnespettro.csv' è stato creato.")

# Chiamata alla funzione per eseguire l'elaborazione
count_female_per_party('partyspettro.csv', 'donnespettro.csv')
