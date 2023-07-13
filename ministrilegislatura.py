import csv

input_file = 'ministriFGL.csv'

# Lettura del file CSV e creazione dei file CSV separati per ogni legislatura
with open(input_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    # Creazione di un dizionario vuoto per tenere traccia dei file CSV per ogni legislatura
    legislatura_files = {}
    
    for row in reader:
        legislatura = row['legislatura']
        
        # Ignora la legislatura "Costituente"
        if legislatura == 'Costituente':
            continue
        
        # Creazione del nome del file CSV per la legislatura corrente
        output_file = f"legislatura_{legislatura}.csv"
        
        # Verifica se il file CSV per la legislatura corrente è già stato aperto, altrimenti aprilo in modalità append
        if legislatura not in legislatura_files:
            legislatura_files[legislatura] = open(output_file, 'w', encoding='utf-8', newline='')
            writer = csv.writer(legislatura_files[legislatura])
            writer.writerow(['Governo', 'Ministro', 'Legislatura'])
        else:
            writer = csv.writer(legislatura_files[legislatura])
        
        # Scrittura della riga corrente nel file CSV appropriato per la legislatura corrente
        writer.writerow([row['Governo'], row['Ministro'], row['legislatura']])

# Chiusura dei file CSV per ogni legislatura
for file in legislatura_files.values():
    file.close()

print("File CSV per ogni legislatura (esclusa la legislatura Costituente) creati con successo.")
