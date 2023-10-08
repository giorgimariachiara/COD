from SPARQLWrapper import JSON
from sparql_dataframe import sparql_dataframe
import pandas as pd
from sparql_dataframe import get
import requests

endpoint = "https://dati.camera.it/sparql"
pd.set_option('display.max_rows', None)


#QUERY QUOTE ROSA 2018: UOMINI 2018 PER GRUPPO PARLAMENTARE 

uomini_2013 ="""SELECT ?gruppoPar (COUNT(DISTINCT ?d) AS ?numeroUomini)
WHERE {SELECT DISTINCT ?d ?cognome ?nome ?legislatura ?gruppoPar ?start
WHERE {
  ## deputato con attributi anagrafici
  ?d a ocd:deputato; 
     foaf:surname ?cognome; 
     foaf:gender "male"; 
     foaf:firstName ?nome;
     ocd:rif_leg ?legislatura; 
     ocd:rif_mandatoCamera ?mandato; 
     ocd:aderisce ?gruppo.

  ## data di inizio mandato
  ?mandato ocd:startDate ?start.
  FILTER (STRSTARTS(?start, "2013"))

  ## etichetta del gruppo a cui aderisce il deputato
  ?gruppo rdfs:label ?gruppoPar.

  ## ruolo del deputato all'interno del gruppo
  ?d ocd:rif_incarico ?incarico.
  ?incarico ocd:ruolo ?gruppoParlamentare.
  FILTER (!STRSTARTS(?gruppoPar, "MISTO"))

  ## escludere i deputati che sono subentrati
  FILTER NOT EXISTS {
    ?mandato ocd:tipoProclamazione ?proclamazione.
    ?proclamazione dc:type "Subentrato alla Camera"
  
   FILTER NOT EXISTS {
    ?mandato ocd:tipoProclamazione ?proclamazione.
    ?proclamazione dc:type "Eletto con suppletiva alla Camera"
  }}}}"""

df_uomini_2013 = get(endpoint, uomini_2013)
df_uomini_2013["gruppoPar"] = df_uomini_2013["gruppoPar"].str.extract(r'^(.*?) \(')
df_uomini_2013= df_uomini_2013.groupby("gruppoPar")["numeroUomini"].sum().reset_index()
print("UOMINI NEL 2013")
print(df_uomini_2013)

uomini_2018 ="""SELECT ?gruppoPar (COUNT(DISTINCT ?d) AS ?numeroUomini)
WHERE {SELECT DISTINCT ?d ?cognome ?nome ?legislatura ?gruppoPar ?start
WHERE {
  ## deputato con attributi anagrafici
  ?d a ocd:deputato; 
     foaf:surname ?cognome; 
     foaf:gender "male"; 
     foaf:firstName ?nome;
     ocd:rif_leg ?legislatura; 
     ocd:rif_mandatoCamera ?mandato; 
     ocd:aderisce ?gruppo.

  ## data di inizio mandato
  ?mandato ocd:startDate ?start.
  FILTER (STRSTARTS(?start, "2018"))

  ## etichetta del gruppo a cui aderisce il deputato
  ?gruppo rdfs:label ?gruppoPar.

  ## ruolo del deputato all'interno del gruppo
  ?d ocd:rif_incarico ?incarico.
  ?incarico ocd:ruolo ?gruppoParlamentare.
  FILTER (!STRSTARTS(?gruppoPar, "MISTO"))

  ## escludere i deputati che sono subentrati
  FILTER NOT EXISTS {
    ?mandato ocd:tipoProclamazione ?proclamazione.
    ?proclamazione dc:type "Subentrato alla Camera"
  
   FILTER NOT EXISTS {
    ?mandato ocd:tipoProclamazione ?proclamazione.
    ?proclamazione dc:type "Eletto con suppletiva alla Camera"
  }}}}"""

df_uomini_2018 = get(endpoint, uomini_2018)
df_uomini_2018["gruppoPar"] = df_uomini_2018["gruppoPar"].str.extract(r'^(.*?) \(')
df_uomini_2018 = df_uomini_2018.groupby("gruppoPar")["numeroUomini"].sum().reset_index()
print("UOMINI NEL 2018")
print(df_uomini_2018)


uomini_2022 ="""SELECT ?gruppoPar (COUNT(DISTINCT ?d) AS ?numeroUomini)
WHERE {SELECT DISTINCT ?d ?cognome ?nome ?legislatura ?gruppoPar ?start
WHERE {
  ## deputato con attributi anagrafici
  ?d a ocd:deputato; 
     foaf:surname ?cognome; 
     foaf:gender "male"; 
     foaf:firstName ?nome;
     ocd:rif_leg ?legislatura; 
     ocd:rif_mandatoCamera ?mandato; 
     ocd:aderisce ?gruppo.

  ## data di inizio mandato
  ?mandato ocd:startDate ?start.
  FILTER (STRSTARTS(?start, "2022"))

  ## etichetta del gruppo a cui aderisce il deputato
  ?gruppo rdfs:label ?gruppoPar.

  ## ruolo del deputato all'interno del gruppo
  ?d ocd:rif_incarico ?incarico.
  ?incarico ocd:ruolo ?gruppoParlamentare.
  FILTER (!STRSTARTS(?gruppoPar, "MISTO"))

  ## escludere i deputati che sono subentrati
  FILTER NOT EXISTS {
    ?mandato ocd:tipoProclamazione ?proclamazione.
    ?proclamazione dc:type "Subentrato alla Camera"
  
   FILTER NOT EXISTS {
    ?mandato ocd:tipoProclamazione ?proclamazione.
    ?proclamazione dc:type "Eletto con suppletiva alla Camera"
  }}}}"""

df_uomini_2022 = get(endpoint, uomini_2022)
df_uomini_2022["gruppoPar"] = df_uomini_2022["gruppoPar"].str.extract(r'^(.*?) \(')
df_uomini_2022 = df_uomini_2022.groupby("gruppoPar")["numeroUomini"].sum().reset_index()
print("UOMINI NEL 2022")
print(df_uomini_2022)



#QUERY QUOTE ROSA 2013: DONNE 2018 PER GRUPPO PARLAMENTARE 

donne_2013 ="""SELECT ?gruppoPar (COUNT(DISTINCT ?d) AS ?numeroDonne)
WHERE {SELECT DISTINCT ?d ?cognome ?nome ?legislatura ?gruppoPar ?start
WHERE {
  ## deputato con attributi anagrafici
  ?d a ocd:deputato; 
     foaf:surname ?cognome; 
     foaf:gender "female"; 
     foaf:firstName ?nome;
     ocd:rif_leg ?legislatura; 
     ocd:rif_mandatoCamera ?mandato; 
     ocd:aderisce ?gruppo.

  ## data di inizio mandato
  ?mandato ocd:startDate ?start.
  FILTER (STRSTARTS(?start, "2013"))

  ## etichetta del gruppo a cui aderisce il deputato
  ?gruppo rdfs:label ?gruppoPar.

  ## ruolo del deputato all'interno del gruppo
  ?d ocd:rif_incarico ?incarico.
  ?incarico ocd:ruolo ?gruppoParlamentare.
  FILTER (!STRSTARTS(?gruppoPar, "MISTO"))

  ## escludere i deputati che sono subentrati
  FILTER NOT EXISTS {
    ?mandato ocd:tipoProclamazione ?proclamazione.
    ?proclamazione dc:type "Subentrato alla Camera"
  
   FILTER NOT EXISTS {
    ?mandato ocd:tipoProclamazione ?proclamazione.
    ?proclamazione dc:type "Eletto con suppletiva alla Camera"
  }}}}"""

df_donne_2013 = get(endpoint, donne_2013)
df_donne_2013["gruppoPar"] = df_donne_2013["gruppoPar"].str.extract(r'^(.*?) \(')
df_donne_2013 = df_donne_2013.groupby("gruppoPar")["numeroDonne"].sum().reset_index()
print("DONNE NEL 2013")
print(df_donne_2013)


donne_2018 ="""SELECT ?gruppoPar (COUNT(DISTINCT ?d) AS ?numeroDonne)
WHERE {SELECT DISTINCT ?d ?cognome ?nome ?legislatura ?gruppoPar ?start
WHERE {
  ## deputato con attributi anagrafici
  ?d a ocd:deputato; 
     foaf:surname ?cognome; 
     foaf:gender "female"; 
     foaf:firstName ?nome;
     ocd:rif_leg ?legislatura; 
     ocd:rif_mandatoCamera ?mandato; 
     ocd:aderisce ?gruppo.

  ## data di inizio mandato
  ?mandato ocd:startDate ?start.
  FILTER (STRSTARTS(?start, "2018"))

  ## etichetta del gruppo a cui aderisce il deputato
  ?gruppo rdfs:label ?gruppoPar.

  ## ruolo del deputato all'interno del gruppo
  ?d ocd:rif_incarico ?incarico.
  ?incarico ocd:ruolo ?gruppoParlamentare.
  FILTER (!STRSTARTS(?gruppoPar, "MISTO"))

  ## escludere i deputati che sono subentrati
  FILTER NOT EXISTS {
    ?mandato ocd:tipoProclamazione ?proclamazione.
    ?proclamazione dc:type "Subentrato alla Camera"
  
   FILTER NOT EXISTS {
    ?mandato ocd:tipoProclamazione ?proclamazione.
    ?proclamazione dc:type "Eletto con suppletiva alla Camera"
  }}}}"""

df_donne_2018 = get(endpoint, donne_2018)
df_donne_2018["gruppoPar"] = df_donne_2018["gruppoPar"].str.extract(r'^(.*?) \(')
df_donne_2018 = df_donne_2018.groupby("gruppoPar")["numeroDonne"].sum().reset_index()
#grouped_df_uomini_2018 = df_uomini_2018.groupby("gruppoPar")["numeroDonne"].sum().reset_index()
print("DONNE NEL 2018")
print(df_donne_2018)


donne_2022 ="""SELECT ?gruppoPar (COUNT(DISTINCT ?d) AS ?numeroDonne)
WHERE {SELECT DISTINCT ?d ?cognome ?nome ?legislatura ?gruppoPar ?start
WHERE {
  ## deputato con attributi anagrafici
  ?d a ocd:deputato; 
     foaf:surname ?cognome; 
     foaf:gender "female"; 
     foaf:firstName ?nome;
     ocd:rif_leg ?legislatura; 
     ocd:rif_mandatoCamera ?mandato; 
     ocd:aderisce ?gruppo.

  ## data di inizio mandato
  ?mandato ocd:startDate ?start.
  FILTER (STRSTARTS(?start, "2022"))

  ## etichetta del gruppo a cui aderisce il deputato
  ?gruppo rdfs:label ?gruppoPar.

  ## ruolo del deputato all'interno del gruppo
  ?d ocd:rif_incarico ?incarico.
  ?incarico ocd:ruolo ?gruppoParlamentare.
  FILTER (!STRSTARTS(?gruppoPar, "MISTO"))

  ## escludere i deputati che sono subentrati
  FILTER NOT EXISTS {
    ?mandato ocd:tipoProclamazione ?proclamazione.
    ?proclamazione dc:type "Subentrato alla Camera"
  
   FILTER NOT EXISTS {
    ?mandato ocd:tipoProclamazione ?proclamazione.
    ?proclamazione dc:type "Eletto con suppletiva alla Camera"
  }}}}"""

df_donne_2022 = get(endpoint, donne_2022)
df_donne_2022["gruppoPar"] = df_donne_2022["gruppoPar"].str.extract(r'^(.*?) \(')
df_donne_2022 = df_donne_2022.groupby("gruppoPar")["numeroDonne"].sum().reset_index()
print(df_donne_2022)




















totale_donne = """
SELECT ?gruppoPar (COUNT(DISTINCT ?d) AS ?numeroDonne)
WHERE {
    {
        SELECT DISTINCT ?d ?cognome ?nome ?legislatura ?gruppoPar ?start
WHERE {
  ## deputato con attributi anagrafici
  ?d a ocd:deputato; 
     foaf:surname ?cognome; 
     foaf:gender "female"; 
     foaf:firstName ?nome;
     ocd:rif_leg ?legislatura; 
     ocd:rif_mandatoCamera ?mandato; 
     ocd:aderisce ?gruppo.

  ## data di inizio mandato
  ?mandato ocd:startDate ?start.
   FILTER (STRSTARTS(?start, "2022"))
  
  ## etichetta del gruppo a cui aderisce il deputato
  ?gruppo rdfs:label ?gruppoPar.
}
    }
}
GROUP BY ?gruppoPar
"""

totale_donne2 = """
SELECT DISTINCT ?d ?cognome ?nome  ?start
WHERE {
  ## deputato con attributi anagrafici
  ?d a ocd:deputato; 
     foaf:surname ?cognome; 
     foaf:gender "male"; 
     foaf:firstName ?nome;
     ocd:rif_leg ?legislatura; 
     ocd:rif_mandatoCamera ?mandato; 
     ocd:aderisce ?gruppo.

  ## data di inizio mandato
  ?mandato ocd:startDate ?start.
   FILTER (STRSTARTS(?start, "2018"))
  
  ## etichetta del gruppo a cui aderisce il deputato
  ?gruppo rdfs:label ?gruppoPar.

  
}
"""

TOTALE = """SELECT DISTINCT ?d ?cognome ?nome ?start
WHERE {
  ## deputato con attributi anagrafici
  ?d a ocd:deputato; 
     foaf:surname ?cognome; 
     foaf:gender "female"; 
     foaf:firstName ?nome;
     ocd:rif_leg ?legislatura; 
     ocd:rif_mandatoCamera ?mandato; 
     ocd:aderisce ?gruppo.

  ## data di inizio mandato
  ?mandato ocd:startDate ?start.
  
  FILTER (STRSTARTS(?start, "2018") || 
          STRSTARTS(?start, "2019") || 
          STRSTARTS(?start, "2020") || 
          STRSTARTS(?start, "2021"))
  
  ## etichetta del gruppo a cui aderisce il deputato
  ?gruppo rdfs:label ?gruppoPar.
}"""
df_totale_donne = get(endpoint, totale_donne)
df_totale_donne2 = get(endpoint, TOTALE)


total_donne = df_totale_donne['numeroDonne'].sum()
#print(total_donne)
print(len(df_totale_donne2))



totale_donne = """
SELECT ?gruppoPar (COUNT(DISTINCT ?d) AS ?numeroDonne)
WHERE {
    {
        SELECT DISTINCT ?d ?cognome ?nome ?legislatura ?gruppoPar ?start
        WHERE {
            ## deputato con attributi anagrafici
            ?d a ocd:deputato; 
               foaf:surname ?cognome; 
               foaf:gender "female"; 
               foaf:firstName ?nome;
               ocd:rif_leg ?legislatura; 
               ocd:rif_mandatoCamera ?mandato; 
               ocd:aderisce ?gruppo.

            ## data di inizio mandato
            ?mandato ocd:startDate ?start.
            FILTER (STRSTARTS(?start, "2022"))

            ## etichetta del gruppo a cui aderisce il deputato
            ?gruppo rdfs:label ?gruppoPar.

            ## ruolo del deputato all'interno del gruppo
            ?d ocd:rif_incarico ?incarico.
            ?incarico ocd:ruolo ?gruppoParlamentare.
        }
    }
}
GROUP BY ?gruppoPar
"""

totale_donne2 = """
SELECT DISTINCT ?d ?cognome ?nome ?legislatura ?gruppoPar ?start
WHERE {
  ## deputato con attributi anagrafici
  ?d a ocd:deputato; 
     foaf:surname ?cognome; 
     foaf:gender "female"; 
     foaf:firstName ?nome;
     ocd:rif_leg ?legislatura; 
     ocd:rif_mandatoCamera ?mandato; 
     ocd:aderisce ?gruppo.

  ## data di inizio mandato
  ?mandato ocd:startDate ?start.
   FILTER (STRSTARTS(?start, "2022"))

  
  ## etichetta del gruppo a cui aderisce il deputato
  ?gruppo rdfs:label ?gruppoPar.

  ## ruolo del deputato all'interno del gruppo
  ?d ocd:rif_incarico ?incarico.
  ?incarico ocd:ruolo ?gruppoParlamentare.
  
}
"""
df_totale_donne = get(endpoint, totale_donne)
df_totale_donne2 = get(endpoint, totale_donne2)


total_donne = df_totale_donne['numeroDonne'].sum()
#print(total_donne)
#print(len(df_totale_donne2))


#controllo per sistemare query 

donne ="""SELECT DISTINCT ?deputato ?cognome ?nome ?dataNascita ?luogoNascita "female" as ?gender
WHERE {
  ?deputato a ocd:deputato;
     ocd:rif_leg ?legislatura;
     ocd:rif_mandatoCamera ?mandato;
     foaf:surname ?cognome;
     foaf:gender "female";
     foaf:firstName ?nome.

  OPTIONAL {
    ?d dc:description ?info.
  }

  OPTIONAL {
    ?d <http://purl.org/vocab/bio/0.1/Birth> ?nascita.
    ?nascita <http://purl.org/vocab/bio/0.1/date> ?dataNascita;
            rdfs:label ?nato;
            ocd:rif_luogo ?luogoNascitaUri.
    ?luogoNascitaUri dc:title ?luogoNascita.
  }
}
"""

df= get(endpoint, donne)
print(len(df))




QUERY="""SELECT DISTINCT ?d ?cognome ?nome ?legislatura ?gruppoPar ?start
WHERE {
  ## deputato con attributi anagrafici
  ?d a ocd:deputato; 
     foaf:surname ?cognome; 
     foaf:gender "female"; 
     foaf:firstName ?nome;
     ocd:rif_leg ?legislatura; 
     ocd:rif_mandatoCamera ?mandato; 
     ocd:aderisce ?gruppo.

  ## data di inizio mandato
  ?mandato ocd:startDate ?start.
  FILTER (STRSTARTS(?start, "2018"))

  ## etichetta del gruppo a cui aderisce il deputato
  ?gruppo rdfs:label ?gruppoPar.
  FILTER (STRSTARTS(?gruppoPar, "MOVIMENTO 5 STELLE"))

  ## ruolo del deputato all'interno del gruppo
  ?d ocd:rif_incarico ?incarico.
  ?incarico ocd:ruolo ?gruppoParlamentare.

  ## escludere i deputati che sono subentrati
  FILTER NOT EXISTS {
    ?mandato ocd:tipoProclamazione ?proclamazione.
    ?proclamazione dc:type "Subentrato alla Camera"
  }
}
"""


querydue ="""SELECT ?gruppoPar (COUNT(DISTINCT ?d) AS ?numeroDonne)
WHERE {SELECT DISTINCT ?d ?cognome ?nome ?legislatura ?gruppoPar ?start
WHERE {
  ## deputato con attributi anagrafici
  ?d a ocd:deputato; 
     foaf:surname ?cognome; 
     foaf:gender "female"; 
     foaf:firstName ?nome;
     ocd:rif_leg ?legislatura; 
     ocd:rif_mandatoCamera ?mandato; 
     ocd:aderisce ?gruppo.

  ## data di inizio mandato
  ?mandato ocd:startDate ?start.
  FILTER (STRSTARTS(?start, "2018"))

  ## etichetta del gruppo a cui aderisce il deputato
  ?gruppo rdfs:label ?gruppoPar.
  FILTER (STRSTARTS(?gruppoPar, "MOVIMENTO 5 STELLE"))

  ## ruolo del deputato all'interno del gruppo
  ?d ocd:rif_incarico ?incarico.
  ?incarico ocd:ruolo ?gruppoParlamentare.

  ## escludere i deputati che sono subentrati
  FILTER NOT EXISTS {
    ?mandato ocd:tipoProclamazione ?proclamazione.
    ?proclamazione dc:type "Subentrato alla Camera"}}}
  """