from SPARQLWrapper import JSON
from sparql_dataframe import sparql_dataframe
import pandas as pd
from sparql_dataframe import get
import requests

endpoint = "https://dati.camera.it/sparql"
pd.set_option('display.max_rows', None)


#QUERY PER TROVARE PARTITO
query_partito_uomini1 = """SELECT DISTINCT ?persona ?cognome ?nome ?dataNascita ?gruppoPar
WHERE {
  ?persona ocd:rif_mandatoCamera ?mandato; a foaf:Person.

  ?d a ocd:deputato;
     ocd:rif_leg ?legislatura;
     ocd:rif_mandatoCamera ?mandato.
  ?d ocd:aderisce ?gruppo.
  ?gruppo rdfs:label ?gruppoPar.

  ## Anagrafica
  ?d foaf:surname ?cognome; foaf:gender "male"; foaf:firstName ?nome.

  OPTIONAL {
    ?persona <http://purl.org/vocab/bio/0.1/Birth> ?nascita.
    ?nascita <http://purl.org/vocab/bio/0.1/date> ?dataNascita;
    rdfs:label ?nato; ocd:rif_luogo ?luogoNascitaUri.
    ?luogoNascitaUri dc:title ?luogoNascita.
  }

  FILTER (?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/costituente>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_01>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_02>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_03>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_04>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_05>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_06>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_07>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_08>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_09>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_10>)
}
"""

query_partito_uomini2 = """SELECT DISTINCT ?persona ?cognome ?nome ?dataNascita ?gruppoPar
WHERE {
  ?persona ocd:rif_mandatoCamera ?mandato; a foaf:Person.

  ?d a ocd:deputato;
     ocd:rif_leg ?legislatura;
     ocd:rif_mandatoCamera ?mandato.
  ?d ocd:aderisce ?gruppo.
  ?gruppo rdfs:label ?gruppoPar.

  ## Anagrafica
  ?d foaf:surname ?cognome; foaf:gender "male"; foaf:firstName ?nome.

  OPTIONAL {
    ?persona <http://purl.org/vocab/bio/0.1/Birth> ?nascita.
    ?nascita <http://purl.org/vocab/bio/0.1/date> ?dataNascita;
    rdfs:label ?nato; ocd:rif_luogo ?luogoNascitaUri.
    ?luogoNascitaUri dc:title ?luogoNascita.
  }

  FILTER (
             ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_11>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_12>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_13>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_14>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_15>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_16>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_17>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_18>
          || ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_19>)
}
"""
query_partito_donne = """SELECT DISTINCT ?persona ?cognome ?nome
?dataNascita ?gruppoPar
WHERE {
?persona ocd:rif_mandatoCamera ?mandato; a foaf:Person.

?d a ocd:deputato;
ocd:rif_leg ?legislatura;
ocd:rif_mandatoCamera ?mandato.
OPTIONAL{?d dc:description ?info}
?d ocd:aderisce ?gruppo .
  ?gruppo rdfs:label ?gruppoPar.

##anagrafica
?d foaf:surname ?cognome; foaf:gender "female" ;foaf:firstName ?nome.
OPTIONAL{
?persona <http://purl.org/vocab/bio/0.1/Birth> ?nascita.
?nascita <http://purl.org/vocab/bio/0.1/date> ?dataNascita;
rdfs:label ?nato; ocd:rif_luogo ?luogoNascitaUri.
?luogoNascitaUri dc:title ?luogoNascita.

}}"""


df_partito_donne = get(endpoint, query_partito_donne)
df_partito_donne['gruppoPar'] = df_partito_donne['gruppoPar'].str.extract(r'^(.*?) \(')
df_partito_donne = df_partito_donne.drop_duplicates(["persona","nome", "cognome", "dataNascita", "gruppoPar"])
df_partito_donne = df_partito_donne[["gruppoPar"]]
df_partito_donne.rename(columns={"gruppoPar": "partito"}, inplace=True)
df_partito_donne = df_partito_donne.assign(gender='female')


df_partito_uomini1 = get(endpoint, query_partito_uomini1)
df_partito_uomini1['gruppoPar'] = df_partito_uomini1['gruppoPar'].str.extract(r'^(.*?) \(')
df_partito_uomini1 = df_partito_uomini1.drop_duplicates(["persona","nome", "cognome", "dataNascita", "gruppoPar"])
df_partito_uomini1 = df_partito_uomini1[["gruppoPar"]]
df_partito_uomini1.rename(columns={"gruppoPar": "partito"}, inplace=True)
df_partito_uomini1 = df_partito_uomini1.assign(gender='male')

df_partito_uomini2 = get(endpoint, query_partito_uomini2)
df_partito_uomini2['gruppoPar'] = df_partito_uomini2['gruppoPar'].str.extract(r'^(.*?) \(')
df_partito_uomini2 = df_partito_uomini2.drop_duplicates(["persona","nome", "cognome", "dataNascita", "gruppoPar"])
df_partito_uomini2 = df_partito_uomini2[["gruppoPar"]]
df_partito_uomini2.rename(columns={"gruppoPar": "partito"}, inplace=True)
df_partito_uomini2 = df_partito_uomini2.assign(gender='male')

df_partito_totale = pd.concat([df_partito_uomini1, df_partito_uomini2, df_partito_donne])

df_partito_totale_no_duplicati = df_partito_totale[["partito"]].drop_duplicates()

listapartiti = df_partito_totale_no_duplicati["partito"].tolist()

print(listapartiti)
print(len(listapartiti))
import pandas as pd

# Leggi il file Excel e crea il DataFrame
df_excel = pd.read_excel('Partiti.xlsx')
listapartiti = [partito.lower().strip() for partito in listapartiti]
df_excel['A'] = df_excel['A'].str.lower().str.strip()

# Crea un dizionario dalla colonna A alla colonna B del DataFrame
mappa_partiti = dict(zip(df_excel['A'], df_excel['B']))

# Itera sulla lista dei partiti
for i in range(len(listapartiti)):
    partito = listapartiti[i]
    if partito in mappa_partiti:
        listapartiti[i] = mappa_partiti[partito]
listapartiti = list(set(listapartiti)) 


print(listapartiti)


from wikidataintegrator import wdi_core
from urllib.parse import quote


from ratelimit import limits, sleep_and_retry
import re
from requests.exceptions import RequestException, TooManyRedirects
@sleep_and_retry
@limits(calls=1, period=2)
def run_sparql_query(query):
    url = 'https://query.wikidata.org/sparql'
    params = {'format': 'json', 'query': query}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'results' in data and 'bindings' in data['results']:
            return data['results']['bindings']
        else:
            print('Risposta JSON non valida: dati mancanti.')
    except (RequestException, TooManyRedirects) as e:
        print(f'Errore nella richiesta HTTP: {str(e)}')
    except json.JSONDecodeError as e:
        print(f'Errore nella decodifica della risposta JSON: {str(e)}')

query_template = '''
SELECT DISTINCT ?party ?partyLabel ?al WHERE {
  {
    ?party wdt:P31 wd:Q7278;
           rdfs:label ?partyLabel;
           wdt:P17 wd:Q38.
    ?party wdt:P1387 ?alignment.
    ?alignment rdfs:label ?al.
  }
  UNION
  {
    ?party wdt:P31 wd:Q6138528;
           rdfs:label ?partyLabel;
           wdt:P17 wd:Q38.
    ?party wdt:P1387 ?alignment.
    ?alignment rdfs:label ?al.
  }
  UNION
  {
    ?party wdt:P31 wd:Q233591;
           rdfs:label ?partyLabel;
           wdt:P17 wd:Q38.
    ?party wdt:P1387 ?alignment.
    ?alignment rdfs:label ?al.
  }
  UNION
  {
    ?party wdt:P31 wd:Q388602;
           rdfs:label ?partyLabel;
           wdt:P17 wd:Q38.
    ?party wdt:P1387 ?alignment.
    ?alignment rdfs:label ?al.
  }
  FILTER(LANG(?partyLabel) = "it")
  FILTER(LANG(?al) = "it")
  FILTER(CONTAINS(LCASE(?partyLabel), LCASE(?search_term)))
}


'''
processed_parties = set()
results_list = []

for partito in listapartiti:
    query = query_template.replace('?search_term', f'"{partito}"')
    results = run_sparql_query(query)

    print(f"Risultati per il partito: {partito}")

    if results:
        for result in results:
            party_label = result['partyLabel']['value']

            # Verifica se il partito è già stato elaborato
            if party_label in processed_parties:
                continue

            processed_parties.add(party_label)  # Aggiungi il partito al set

            alignment_label = result.get('al', {}).get('value', '')  # Estrai l'allineamento politico

            print(f"Partito: {party_label}")
            print(f"Allineamento: {alignment_label}")

            results_list.append({'Partito': party_label, 'Allineamento Politico': alignment_label})
    else:
        print("Nessun risultato trovato")

    print()


    # Creazione del dataframe
df = pd.DataFrame(results_list)
partiti_trovati = [result['Partito'] for result in results_list]

print(partiti_trovati)



partiti_trovati = df['Partito'].tolist()
partiti_non_trovati = [partito for partito in listapartiti if partito not in partiti_trovati]
df_filtered = df[df['Partito'].isin(listapartiti)]

from urllib.parse import urlencode
@sleep_and_retry
@limits(calls=1, period=2)
def run_sparql_query(query):
    url = 'https://query.wikidata.org/sparql'
    params = {'format': 'json', 'query': query}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'results' in data and 'bindings' in data['results']:
            return data['results']['bindings']
        else:
            print('Risposta JSON non valida: dati mancanti.')
    except (RequestException, TooManyRedirects) as e:
        print(f'Errore nella richiesta HTTP: {str(e)}')
    except json.JSONDecodeError as e:
        print(f'Errore nella decodifica della risposta JSON: {str(e)}')

# Definizione del template della query
query_template2 = '''
SELECT DISTINCT ?party ?partyLabel ?result WHERE {{
  ?party wdt:P31 wd:Q7278;
         rdfs:label ?partyLabel;
         wdt:P17 wd:Q38;
         wdt:P1142 ?politicalideology.
  ?politicalideology rdfs:label ?politicalideologylabel.
  OPTIONAL {{
    ?politicalideology wdt:P1387 ?alignment.
    ?alignment rdfs:label ?al.
    FILTER(LANG(?al) = "it")
  }}
  BIND(COALESCE(?al, ?politicalideologylabel) AS ?result)
  FILTER(LANG(?partyLabel) = "it")
  FILTER(CONTAINS(?partyLabel, "{search_term}"))
  FILTER(LANG(?result) = "it")
}}
'''
processed_parties2 = set()  # Set per tenere traccia dei partiti elaborati
results_list2 = []  # Lista per salvare i risultati dei partiti e allineamenti

for partito in partiti_non_trovati:
    # Verifica se il partito è già presente nel DataFrame
    if partito in results_list2:
        continue

    query = query_template2.format(search_term=partito)
    # Esegui la query SPARQL e ottieni i risultati
    # Assumi che tu abbia una funzione `run_sparql_query()` che esegue la query SPARQL
    results = run_sparql_query(query)

    print(f"Risultati per il partito: {partito}")

    if results:
      for result in results:
          party_label = result['partyLabel']['value']

          # Verifica se il partito è già stato elaborato
          if party_label in processed_parties:
              continue

          processed_parties2.add(party_label)  # Aggiungi il partito al set

          alignment_label = result.get('result', {}).get('value', '')  # Estrai l'allineamento politico

          print(f"Partito: {party_label}")
          print(f"Allineamento: {alignment_label}")

          results_list2.append({'Partito': party_label, 'Allineamento Politico': alignment_label})
          break  # Esci dal ciclo dopo aver aggiunto il primo valore

    else:
        print("Nessun risultato trovato")
# Creazione del dataframe con i risultati dei partiti senza allineamenti politici
df_risultati2 = pd.DataFrame(results_list2)

partiti_trovati = df_risultati2['Partito'].tolist()
partiti_non_trovati = [partito for partito in listapartiti if partito not in partiti_trovati]
df_filtered2 = df_risultati2[df_risultati2['Partito'].isin(listapartiti)]

df_alignment_partiti = pd.concat([df_filtered, df_filtered2])

#print(df_alignment_partiti)

df_merged = df_partito_totale.merge(df_excel.assign(A=df_excel['A'].str.lower(), B=df_excel['B'].str.upper()), left_on=df_partito_totale['partito'].str.lower(), right_on='A', how='left')
df_merged['partito'] = df_merged['B'].combine_first(df_merged['partito']).str.upper()
df_merged = df_merged.drop(['A', 'B'], axis=1)

print(df_merged)
df_merged['partito'] = df_merged['partito'].str.upper()
df_alignment_partiti['Partito'] = df_alignment_partiti['Partito'].str.upper()

df_completo_alignment = df_merged.merge(df_alignment_partiti, left_on='partito', right_on='Partito', how='left')
df_completo_alignment.drop(columns=['Partito'], inplace=True)


keyword_mapping = {
    "repubblicanesimo": "centro",
    "socialismo": "sinistra",
    "conservatorismo": "destra",
    "cristianesimo democratico": "centro"
}

df_completo_alignment['Allineamento Politico'] = df_completo_alignment['Allineamento Politico'].apply(lambda x: keyword_mapping.get(x, x))
df_completo_alignment = df_completo_alignment[df_completo_alignment['partito'] != 'MISTO']
print(df_completo_alignment)
