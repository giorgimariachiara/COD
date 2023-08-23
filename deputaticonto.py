import csv

# Apri il file CSV di input
with open('totaledeputati.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Salta l'intestazione del file

    # Inizializza i contatori
    count_male = 0
    count_female = 0

    # Conta il numero di deputati uomini e donne
    for row in reader:
        gender = row[2].strip().lower()  # Assumi che la colonna "gender" sia la terza colonna (indice 2)
        if gender == 'male':
            count_male += 1
        elif gender == 'female':
            count_female += 1

# Crea un nuovo file CSV con i risultati
with open('totdep.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Scrivi l'intestazione
    writer.writerow(['gender', 'count'])

    # Scrivi i dati
    writer.writerow(['male', count_male])
    writer.writerow(['female', count_female])

print("Elaborazione completata. Il file 'totdep.csv' è stato creato.")


#conto totale presenza deputati maschi e femmine per chart tot su html. 