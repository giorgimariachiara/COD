import csv

# Funzione per ottenere il numero di legislatura dal link RDF
def get_legislatura_from_url(url):
    if url.endswith("costituente"):
        return "legislatura costituente"
    else:
        return "legislatura " + url.split("_")[-1]

# Percorso del file CSV di input
input_file = 'ministri.csv'
# Percorso del file CSV di output
output_file = 'ministri3.csv'

# Apertura dei file di input e output
with open(input_file, 'r') as csv_input, open(output_file, 'w', newline='') as csv_output:
    reader = csv.DictReader(csv_input)
    fieldnames = [field for field in reader.fieldnames if field != 'legislatura']  # Fieldnames senza la colonna "legislatura"
    fieldnames.append('legislatura_modificata')  # Aggiunta della colonna "legislatura_modificata"

    writer = csv.DictWriter(csv_output, fieldnames=fieldnames)
    writer.writeheader()

    # Scrittura delle righe nel file di output con la colonna "legislatura_modificata" modificata
    for row in reader:
        legislatura_url = row['legislatura']
        legislatura_modificata = get_legislatura_from_url(legislatura_url)
        del row['legislatura']  # Rimozione della colonna "legislatura"
        row['legislatura_modificata'] = legislatura_modificata
        writer.writerow(row)

print("Conversione completata!")
