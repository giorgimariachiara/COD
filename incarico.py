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

"""
qui conta





#cambia formato legislature 

import pandas as pd

# Dizionario per associare i numeri alle legislature
legislature_dict = {
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_01': 1,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_02': 2,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_03': 3,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_10': 10,
    'http://dati.camera.it/ocd/legislatura.rdf/costituente': 'Costituente',
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_17': 17,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_18': 18,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_05': 5,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_07': 7,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_04': 4,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_08': 8,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_09': 9,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_06': 6,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_11': 11,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_13': 13,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_15': 15,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_16': 16,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_14': 14,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_12': 12,
    'http://dati.camera.it/ocd/legislatura.rdf/repubblica_19': 19,
}

# Carica i dati degli incarichi per uomini e donne dai file CSV
df_uomini = pd.read_csv('incaricouomini.csv')
df_donne = pd.read_csv('incaricodonne.csv')

# Modifica le colonne delle legislature nei DataFrame con i numeri associati
df_uomini['legislatura'] = df_uomini['legislatura'].map(legislature_dict)
df_donne['legislatura'] = df_donne['legislatura'].map(legislature_dict)

# Salva i DataFrame con i dati modificati in due nuovi file CSV
df_uomini.to_csv('incaricoMALE.csv', index=False)
df_donne.to_csv('incaricoFEMALE.csv', index=False)
"""