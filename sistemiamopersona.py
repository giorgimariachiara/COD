# MALE EDUCATION ANALYSIS
from SPARQLWrapper import SPARQLWrapper, JSON
import sparql_dataframe
import pandas as pd
from sparql_dataframe import get
import requests
from bs4 import BeautifulSoup
import re
import os
import urllib.parse
import wikipediaapi

"""
endpoint = "https://dati.camera.it/sparql"
pd.set_option('display.max_rows', None)
querydefinitivalaureauomini =SELECT DISTINCT ?persona ?cognome ?nome ?info
?dataNascita ?luogoNascita ?legislatura
WHERE {
?persona ocd:rif_mandatoCamera ?mandato; a foaf:Person.

?d a ocd:deputato;
ocd:rif_leg ?legislatura;
ocd:rif_mandatoCamera ?mandato.
OPTIONAL{?d dc:description ?info}

##anagrafica
?d foaf:surname ?cognome; foaf:gender "male" ;foaf:firstName ?nome; ocd:rif_leg ?legislatura.
OPTIONAL{
?persona <http://purl.org/vocab/bio/0.1/Birth> ?nascita.
?nascita <http://purl.org/vocab/bio/0.1/date> ?dataNascita;
rdfs:label ?nato; ocd:rif_luogo ?luogoNascitaUri.
?luogoNascitaUri dc:title ?luogoNascita.

FILTER (?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/costituente> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_01> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_02> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_03> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_04> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_05> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_06> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_07> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_08> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_09> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_10>)
}}



df_laurea_uomini = get(endpoint, querydefinitivalaureauomini)
df_laurea_uomini = df_laurea_uomini.drop_duplicates(["persona","nome", "cognome","legislatura"]) #5204
#df_laurea_uomini_data = df_laurea_uomini.drop_duplicates(["persona","nome", "cognome", "dataNascita","luogoNascita"])

print(df_laurea_uomini)


def capitalize_name(name):
    parts = re.findall(r"[\w'-]+", name)
    capitalized_parts = [part.capitalize() for part in parts]
    return "_".join(capitalized_parts)


df_laurea_uomini['Persona'] = df_laurea_uomini['nome'].apply(capitalize_name) + "_" + df_laurea_uomini['cognome'].apply(capitalize_name)
df_laurea_uomini1 = df_laurea_uomini[["Persona", "legislatura"]]
print(df_laurea_uomini1)

querydefinitivalaureauomini2 =SELECT DISTINCT ?persona ?cognome ?nome ?info
?dataNascita ?luogoNascita ?legislatura
WHERE {
?persona ocd:rif_mandatoCamera ?mandato; a foaf:Person.

?d a ocd:deputato;
ocd:rif_leg ?legislatura;
ocd:rif_mandatoCamera ?mandato.
OPTIONAL{?d dc:description ?info}

##anagrafica
?d foaf:surname ?cognome; foaf:gender "male" ;foaf:firstName ?nome; ocd:rif_leg ?legislatura.
OPTIONAL{
?persona <http://purl.org/vocab/bio/0.1/Birth> ?nascita.
?nascita <http://purl.org/vocab/bio/0.1/date> ?dataNascita;
rdfs:label ?nato; ocd:rif_luogo ?luogoNascitaUri.
?luogoNascitaUri dc:title ?luogoNascita.

FILTER (?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_11> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_12> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_13> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_14> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_15> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_16> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_17> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_18> ||
          ?legislatura = <http://dati.camera.it/ocd/legislatura.rdf/repubblica_19>)
}}



df_laurea_uomini2 = get(endpoint, querydefinitivalaureauomini2)
df_laurea_uomini2 = df_laurea_uomini2.drop_duplicates(["persona","nome", "cognome","legislatura"]) #5204
#df_laurea_uomini_data = df_laurea_uomini.drop_duplicates(["persona","nome", "cognome", "dataNascita","luogoNascita"])

print(df_laurea_uomini2)


def capitalize_name(name):
    parts = re.findall(r"[\w'-]+", name)
    capitalized_parts = [part.capitalize() for part in parts]
    return "_".join(capitalized_parts)


df_laurea_uomini2['Persona'] = df_laurea_uomini2['nome'].apply(capitalize_name) + "_" + df_laurea_uomini2['cognome'].apply(capitalize_name)
df_laurea_uomini2 = df_laurea_uomini2[["Persona", "legislatura"]]
print(df_laurea_uomini2)

df_unified = pd.concat([df_laurea_uomini2, df_laurea_uomini], ignore_index=True)



querydefinitivalaureadonne =SELECT DISTINCT ?persona ?cognome ?nome ?info
?dataNascita ?luogoNascita ?legislatura
WHERE {
?persona ocd:rif_mandatoCamera ?mandato; a foaf:Person.

?d a ocd:deputato;
ocd:rif_leg ?legislatura;
ocd:rif_mandatoCamera ?mandato.
OPTIONAL{?d dc:description ?info}

##anagrafica
?d foaf:surname ?cognome; foaf:gender "female" ;foaf:firstName ?nome; ocd:rif_leg ?legislatura.
OPTIONAL{
?persona <http://purl.org/vocab/bio/0.1/Birth> ?nascita.
?nascita <http://purl.org/vocab/bio/0.1/date> ?dataNascita;
rdfs:label ?nato; ocd:rif_luogo ?luogoNascitaUri.
?luogoNascitaUri dc:title ?luogoNascita.
}}



df_laurea_donne = get(endpoint, querydefinitivalaureadonne)
df_laurea_donne = df_laurea_donne.drop_duplicates(["persona","nome", "cognome","legislatura"]) #5204
#df_laurea_uomini_data = df_laurea_uomini.drop_duplicates(["persona","nome", "cognome", "dataNascita","luogoNascita"])

#print(df_laurea_donne)


def capitalize_name(name):
    parts = re.findall(r"[\w'-]+", name)
    capitalized_parts = [part.capitalize() for part in parts]
    return "_".join(capitalized_parts)


df_laurea_donne['Persona'] = df_laurea_donne['nome'].apply(capitalize_name) + "_" + df_laurea_donne['cognome'].apply(capitalize_name)
df_laurea_donne = df_laurea_donne[["Persona", "legislatura"]]

df_finale = pd.concat([df_laurea_donne, df_unified], ignore_index=True)
df_finale = df_finale[["Persona", "legislatura"]]
df_finale.to_csv('totaledeputatiperlegislatura.csv', index=False)
 #print(df_finale)

"""
df = pd.read_csv('mergedgraduationtot.csv')

# Seleziona solo le colonne 'Persona' e 'graduated'
df_selected = df[['Persona', 'graduated']]

# Salva il risultato in un nuovo file CSV
df_selected.to_csv('mergedgraduationtot2.csv', index=False)
