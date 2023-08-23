"""
vorrei un codice py che mi modificasse entrambi i csv con gli stessi cambiamenti, ovvero:
1: vorrei che fosse eliminata la prima colonna, "d" elimina ovviamente anche tutte le righe corrispondenti.
2: nella colonna "legislatura" vorrei che il formato di queste ultime fosse 1 2 3 ecc

import pandas as pd

def transform_legislatura(url):
    if "costituente" in url:
        return "costituente"
    else:
        num = url.split("_")[-1]
        return str(int(num)) if num.startswith("0") and len(num) > 1 else num

def modify_csv(input_filename, output_filename):
    df = pd.read_csv(input_filename)
    
    # Rimuovi la prima colonna 'd'
    df = df.drop(columns=['d'])
    
    # Modifica il formato della colonna 'legislatura'
    df['legislatura'] = df['legislatura'].apply(transform_legislatura)
    
    # Salva il DataFrame modificato in un nuovo CSV
    df.to_csv(output_filename, index=False)

# Modifica il file delle donne deputate
modify_csv("gpincaricodonne.csv", "gpincaricoFE.csv")

# Modifica il file degli uomini deputati
modify_csv("gpincaricouomini.csv", "gpincaricoMA.csv")


"""
"""
# avere un codice py che mi conti i deputati che ricoprono ogni ruolo presente nella colonna gruppoParlamentare, mantenendo il filtro per legislatura 

import pandas as pd

def transform_legislatura(url):
    if "costituente" in url:
        return "costituente"
    else:
        num = url.split("_")[-1]
        return str(int(num))

def count_roles_by_legislatura(input_filename, output_filename):
    df = pd.read_csv(input_filename)
    
    # Modifica il formato della colonna 'legislatura'
    df['legislatura'] = df['legislatura'].apply(transform_legislatura)
    
    # Ordina le legislature in modo cronologico
    legislatures = ['costituente'] + [str(i) for i in range(1, 20)]
    df['legislatura'] = pd.Categorical(df['legislatura'], categories=legislatures, ordered=True)
    
    # Raggruppa per legislatura e ruolo, quindi conta i deputati
    role_counts = df.groupby(['legislatura', 'gruppoParlamentare']).size().reset_index(name='count')
    
    # Salva i conteggi in un nuovo file CSV
    role_counts.to_csv(output_filename, index=False)

count_roles_by_legislatura("gpincaricodonne.csv", "CgpincaricoFE.csv")

"""
"""
#lo stesso ma per gli uomini 
import pandas as pd

def transform_legislatura(url):
    if "costituente" in url:
        return "costituente"
    else:
        num = url.split("_")[-1]
        return str(int(num))

def count_roles_by_legislatura(input_filename, output_filename):
    df = pd.read_csv(input_filename)
    
    # Modifica il formato della colonna 'legislatura'
    df['legislatura'] = df['legislatura'].apply(transform_legislatura)
    
    # Ordina le legislature in modo cronologico
    legislatures = ['costituente'] + [str(i) for i in range(1, 20)]
    df['legislatura'] = pd.Categorical(df['legislatura'], categories=legislatures, ordered=True)
    
    # Raggruppa per legislatura e ruolo, quindi conta i deputati
    role_counts = df.groupby(['legislatura', 'gruppoParlamentare']).size().reset_index(name='count')
    
    # Salva i conteggi in un nuovo file CSV
    role_counts.to_csv(output_filename, index=False)

count_roles_by_legislatura("gpincaricouomini.csv", "CgpincaricoMA.csv")


"""
import pandas as pd

# Carica i dati dal file CSV
df = pd.read_csv("CgpincaricoFE.csv")

# Ottieni le categorie uniche dalla colonna 'gruppoParlamentare'
unique_categories = df['gruppoParlamentare'].unique()

# Calcola il numero totale di categorie di incarichi
num_categories = len(unique_categories)

print("Numero totale di categorie di incarichi:", num_categories)
print("Nomi delle categorie di incarichi uniche:")
for category in unique_categories:
    print(category)
