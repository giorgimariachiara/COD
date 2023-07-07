import csv

def conto_incarichi_per_legislatura(file_csv, output_csv):
    conto_incarichi = {}

    with open(file_csv, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            legislatura = row['legislatura']
            incarico = row['incarico']
            
            if legislatura in conto_incarichi:
                if incarico in conto_incarichi[legislatura]:
                    conto_incarichi[legislatura][incarico] += 1
                else:
                    conto_incarichi[legislatura][incarico] = 1
            else:
                conto_incarichi[legislatura] = {incarico: 1}
    
    with open(output_csv, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['legislatura', 'incarico', 'conto'])
        
        for legislatura in sorted(conto_incarichi.keys()):
            incarichi = conto_incarichi[legislatura]
            for incarico in incarichi:
                conto = incarichi[incarico]
                writer.writerow([legislatura, incarico, conto])

# Esempio di utilizzo per il file incaricouomini.csv
conto_incarichi_per_legislatura('incaricouomini.csv', 'contoincaricoMA.csv')

# Esempio di utilizzo per il file incaricodonne.csv
conto_incarichi_per_legislatura('incaricodonne.csv', 'contoincaricoFE.csv')
