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

endpoint = "https://dati.camera.it/sparql"
pd.set_option('display.max_rows', None)

querylaureadonne ="""SELECT DISTINCT ?persona ?cognome ?nome ?info
?dataNascita ?luogoNascita
WHERE {
?persona ocd:rif_mandatoCamera ?mandato; a foaf:Person.

?d a ocd:deputato;
ocd:rif_leg ?legislatura;
ocd:rif_mandatoCamera ?mandato.
OPTIONAL{?d dc:description ?info}

##anagrafica
?d foaf:surname ?cognome; foaf:gender "female" ;foaf:firstName ?nome.
OPTIONAL{
?persona <http://purl.org/vocab/bio/0.1/Birth> ?nascita.
?nascita <http://purl.org/vocab/bio/0.1/date> ?dataNascita;
rdfs:label ?nato; ocd:rif_luogo ?luogoNascitaUri.
?luogoNascitaUri dc:title ?luogoNascita.
}}"""

df_laurea_donne = get(endpoint, querylaureadonne)
df_laurea_donne = df_laurea_donne.drop_duplicates(["persona","nome", "cognome", "dataNascita"])

df_donne_noinfo = df_laurea_donne[df_laurea_donne['info'].isna()]
df_donne_noinfo_data = df_donne_noinfo[["nome", "cognome", "dataNascita"]]

import locale
from datetime import datetime

os.environ['LC_TIME'] = 'it_IT.utf-8'

# Dizionario per mappare i nomi dei mesi in italiano
mesi_italiani = {
    'January': 'gennaio',
    'February': 'febbraio',
    'March': 'marzo',
    'April': 'aprile',
    'May': 'maggio',
    'June': 'giugno',
    'July': 'luglio',
    'August': 'agosto',
    'September': 'settembre',
    'October': 'ottobre',
    'November': 'novembre',
    'December': 'dicembre'
}
lista_politici_data_nascita = []

def capitalize_name(name):
    parts = re.split(r"([ '-])", name)
    return "".join([part.capitalize() for part in parts])

for index, row in df_donne_noinfo_data.iterrows():
    nome = row['nome'].split()
    cognome = row['cognome'].split()
    nome_cognome = "_".join([capitalize_name(word) for word in nome + cognome])
    data_nascita = row['dataNascita']
    if pd.notna(data_nascita):
        data = datetime.strptime(str(int(data_nascita)), "%Y%m%d")
        giorno = str(data.day)  # Converte il giorno in stringa
        mese_in_inglese = data.strftime("%B")
        mese = mesi_italiani.get(mese_in_inglese, mese_in_inglese)
        anno = str(data.year)  # Converte l'anno in stringa
        data_formattata = f"{giorno} {mese} {anno}"
        lista_politici_data_nascita.append((nome_cognome, data_formattata))
    else:
        lista_politici_data_nascita.append((nome_cognome, ""))

df_laurea_donne['info'] = df_laurea_donne['info'].fillna('')
masklaurea = df_laurea_donne['info'].str.contains('Laurea|laurea|Master|LAUREA')

# Estrazione delle persone che hanno laurea dai dati di dati camera
laureate = df_laurea_donne[masklaurea]
laureate = laureate.assign(gender='female')
donnelaureate = laureate[["nome", "cognome", "gender"]]
def capitalize_name(name):
    parts = re.findall(r"[\w'-]+", name)
    capitalized_parts = [part.capitalize() for part in parts]
    return "_".join(capitalized_parts)

for index, row in donnelaureate.iterrows():
    nome = row['nome']
    cognome = row['cognome']
    persona = capitalize_name(nome) + "_" + capitalize_name(cognome)
    donnelaureate.at[index, 'Persona'] = persona

# Seleziona solo le colonne desiderate
donnelaureate = donnelaureate[['Persona', 'gender']]

masknonlaurea =~df_laurea_donne['info'].str.contains('Laurea|laurea|Master|LAUREA', na=False) & df_laurea_donne['info'].ne('')
donnenonlaureate = df_laurea_donne[masknonlaurea]
donnenonlaureate = donnenonlaureate.assign(gender='female')
donnenonlaureate = donnenonlaureate[["nome", "cognome", "gender"]]

def capitalize_name(name):
    parts = re.findall(r"[\w'-]+", name)
    capitalized_parts = [part.capitalize() for part in parts]
    return "_".join(capitalized_parts)

for index, row in donnenonlaureate.iterrows():
    nome = row['nome']
    cognome = row['cognome']
    persona = capitalize_name(nome) + "_" + capitalize_name(cognome)
    donnenonlaureate.at[index, 'Persona'] = persona

# Seleziona solo le colonne desiderate
donnenonlaureate = donnenonlaureate[['Persona', 'gender']]

print("DONNE TOTALE 905")
print(len(df_laurea_donne))
print("DONNE LAUREATE 569")
print(len(donnelaureate))
print("DONNE NO INFO 49")
print(len(df_donne_noinfo))
print("DONNE NON LAUREATE 287")
print(len(donnenonlaureate))

#CERCA PAGINA WIKIPEDIA DELLE PERSONE SENZA INFORMAZIONI SUL TITOLO DI STUDIO

import re
from bs4 import BeautifulSoup

def check_url_exists(url):
    response = requests.get(url)
    return response.status_code == 200

def extract_birth_date(text):
    if '–' in text:
        date_range = re.findall(r'(\d+\s\w+\s\d+)', text)
        if date_range:
            birth_date = date_range[0]
            if birth_date in text.split('–')[0]:
                return birth_date
    else:
        matches = re.findall(r'(\d+\s\w+\s\d+)', text)
        if matches:
            return matches[0]
    return None

url_lista = []
donne_con_url = []
donne_senza_url = []

for nome_cognome, data_nascita in lista_politici_data_nascita:
    url_politico_data = None
    for anno_iniziale in [1952, 1940, 1929]:
        url_politico_data = f"https://it.wikipedia.org/wiki/{nome_cognome}_(politico_{anno_iniziale})"
        if check_url_exists(url_politico_data):
            pagina_wikipedia = requests.get(url_politico_data)
            if pagina_wikipedia.status_code == 200:
                soup = BeautifulSoup(pagina_wikipedia.text, 'html.parser')
                paragraph = soup.find('p')
                if paragraph:
                    birth_date = extract_birth_date(paragraph.text)
                    if birth_date and (birth_date == data_nascita or birth_date.split(' – ')[0] == data_nascita):
                        #print(f"URL della pagina di Wikipedia per {nome_cognome} (politico con data): {url_politico_data}")
                        url_lista.append(url_politico_data)
                        donne_con_url.append(nome_cognome)
                        break
                else:
                    print("Paragrafo non trovato.")
    else:
        url_politico = f"https://it.wikipedia.org/wiki/{nome_cognome}_(politico)"
        url_generale = f"https://it.wikipedia.org/wiki/{nome_cognome}"
        if check_url_exists(url_politico):
            pagina_wikipedia = requests.get(url_politico)
            if pagina_wikipedia.status_code == 200:
                soup = BeautifulSoup(pagina_wikipedia.text, 'html.parser')
                paragraph = soup.find('p')
                if paragraph:
                    birth_date = extract_birth_date(paragraph.text)
                    if birth_date and (birth_date == data_nascita or birth_date.split(' – ')[0] == data_nascita):
                        #print(f"URL della pagina di Wikipedia per {nome_cognome} (politico): {url_politico}")
                        url_lista.append(url_politico)
                        donne_con_url.append(nome_cognome)
                        continue
                else:
                    print("Paragrafo non trovato.")
        if check_url_exists(url_generale):
            pagina_wikipedia = requests.get(url_generale)
            if pagina_wikipedia.status_code == 200:
                soup = BeautifulSoup(pagina_wikipedia.text, 'html.parser')
                paragraph = soup.find('p')
                if paragraph:
                    birth_date = extract_birth_date(paragraph.text)
                    if birth_date and (birth_date == data_nascita or birth_date.split(' – ')[0] == data_nascita):
                        #print(f"URL della pagina di Wikipedia generica per {nome_cognome}: {url_generale}")
                        url_lista.append(url_generale)
                        donne_con_url.append(nome_cognome)
                        continue
                else:
                    print("Paragrafo non trovato.")
        print(f"Nessun URL trovato per {nome_cognome}")

        donne_senza_url.append((nome_cognome, data_nascita))


df_donne_con_url = pd.DataFrame({"Persona": donne_con_url, "URL": url_lista})
for index, row in df_donne_con_url.iterrows():
    persona = row["Persona"]
    for nome_cognome, data_nascita in lista_politici_data_nascita:
        if nome_cognome == persona:
            df_donne_con_url.at[index, "Data di nascita"] = data_nascita
            break

df_donne_senza_url = pd.DataFrame({"Persona e Data di nascita": donne_senza_url})
pd.set_option('display.max_colwidth', None)


print("Donne che hanno url subito 30")
print(len(df_donne_con_url))
print("Donne senza url subito 19")
print(len(df_donne_senza_url))


lista_donne_senza_url = df_donne_senza_url['Persona e Data di nascita'].values.tolist()

import pandas as pd
import wikipediaapi
import re

#Stesso controllo ma per vedere le date primo e per quelli che sono morti e quindi hanno due date su cui fare il check ecc

def extract_birth_date(text):
    if '–' in text:
        date_range = re.findall(r'(\d+\s\w+\s\d+)', text)
        if date_range:
            birth_date = date_range[0]
            if birth_date in text.split('–')[0]:
                return birth_date
    else:
        matches = re.findall(r'(\d+º?\s\w+\s\d+)', text)
        if matches:
            birth_date = matches[0]
            if birth_date.startswith('1º'):
                return birth_date.replace('º', '')
            return birth_date

def find_wikipedia_url(nome_cognome, data_nascita):
    headers = {
        'User-Agent': 'My Wikipedia Script (elizastuglik@gmail.com)'
    }

    wiki_wiki = wikipediaapi.Wikipedia("it", headers=headers)

    url_politico_data = None
    url_politico = None
    url_generale = None

    for anno_iniziale in [1952, 1940, 1929]:
        page_name = f"{nome_cognome} (politico {anno_iniziale})"
        page = wiki_wiki.page(page_name)
        if page.exists():
            content = page.text
            birth_date = extract_birth_date(content)
            if birth_date and (birth_date == data_nascita or birth_date.split(' – ')[0] == data_nascita):
                url_politico_data = page.fullurl
                break

    if not url_politico_data:
        page_name = f"{nome_cognome} (politico)"
        page = wiki_wiki.page(page_name)
        if page.exists():
            content = page.text
            birth_date = extract_birth_date(content)
            if birth_date and (birth_date == data_nascita or birth_date.split(' – ')[0] == data_nascita):
                url_politico = page.fullurl

    if not url_politico_data and not url_politico:
        page_name = nome_cognome
        page = wiki_wiki.page(page_name)
        if page.exists():
            content = page.text
            birth_date = extract_birth_date(content)
            if birth_date and (birth_date == data_nascita or birth_date.split(' – ')[0] == data_nascita):
                url_generale = page.fullurl

    if url_politico_data:
        return (nome_cognome, data_nascita, url_politico_data)
    elif url_politico:
        return (nome_cognome, data_nascita, url_politico)
    elif url_generale:
        return (nome_cognome, data_nascita, url_generale)
    else:
        return (nome_cognome, data_nascita, None)

df_with_url = pd.DataFrame(columns=['Nome', 'Data di nascita', 'URL'])
df_without_url = pd.DataFrame(columns=['Nome', 'Data di nascita'])

for item in lista_donne_senza_url:
    nome_cognome, data_nascita, url = find_wikipedia_url(item[0], item[1])
    if url:
        df_with_url = pd.concat([df_with_url, pd.DataFrame({'Nome': [nome_cognome], 'Data di nascita': [data_nascita], 'URL': [url]})], ignore_index=True)
    else:
        df_without_url = pd.concat([df_without_url, pd.DataFrame({'Nome': [nome_cognome], 'Data di nascita': [data_nascita]})], ignore_index=True)

pd.set_option('display.max_colwidth', None)

print("DONNE CON URL DOPO IL PRIMO TENT 5:")
print(df_with_url)
print(len(df_with_url))
print("DONNE SENZA URL ANCHE DOPO QUESTO TENT 14:")
print(df_without_url)
print(len(df_without_url))


#Trovare quelli che hanno dei secondi nomi su wiki ecc

# Funzione per controllare l'esistenza dell'URL
def check_url_exists(url):
    response = requests.get(url)
    return response.status_code == 200

# Funzione per ottenere URL alternativi
def get_alternative_urls(nome, cognome):
    search_query = f"https://it.wikipedia.org/w/index.php?title=Speciale:Search&search={nome}+{cognome}"
    search_response = requests.get(search_query)

    alternative_urls = []

    if search_response.status_code == 200:
        search_soup = BeautifulSoup(search_response.content, "html.parser")
        search_results = search_soup.find_all("div", class_="mw-search-result-heading")

        for result in search_results:
            result_link = result.find("a")
            result_url = result_link["href"]
            url = f"https://it.wikipedia.org{result_url}"
            decoded_url = urllib.parse.unquote(url)  # Decodifica l'URL per visualizzare i caratteri speciali
            alternative_urls.append(decoded_url)

    return alternative_urls

url_lista = []
donne_con_url2 = []
donne_senza_url2 = []
date_nascita_senza_url2 = []
date_nascita_con_url2 = []

for index, row in df_without_url.iterrows():
    persona = row['Nome']
    nome_cognome_parts = persona.split("_")
    nome = nome_cognome_parts[0]
    cognome = nome_cognome_parts[-1]

    response = requests.get(f"https://it.wikipedia.org/wiki/{persona}", timeout=10)

    if response.status_code == 200:
        url_lista.append(response.url)
        donne_con_url2.append(persona)
        date_nascita_con_url2.append(row['Data di nascita'])
    else:
        alternative_urls = get_alternative_urls(nome, cognome)

        for alternative_url in alternative_urls:
            if check_url_exists(alternative_url):
                url_lista.append(alternative_url)
                donne_con_url2.append(persona)
                date_nascita_con_url2.append(row['Data di nascita'])
                break
        else:
            donne_senza_url2.append(persona)
            date_nascita_senza_url2.append(row['Data di nascita'])

df_donne_con_url2 = pd.DataFrame({"Persona": donne_con_url2, "URL": url_lista, "Data di nascita": date_nascita_con_url2})
df_donne_senza_url2 = pd.DataFrame({"Persona": donne_senza_url2, "Data di nascita": date_nascita_senza_url2})

print("Lunghezza dataframe donne con URL 14:")
print(len(df_donne_con_url2))
print(df_donne_con_url2)
print("Lunghezza dataframe donne senza URL 0:")
print(len(df_donne_senza_url2))
print(df_donne_senza_url2)

#Controlliamo se nell'url c'è effettivamente il nome o il cognome
corresponding_rows = []
non_corresponding_rows = []

for _, row in df_donne_con_url2 .iterrows():
    nome_cognome = row['Persona']
    url = row['URL']

    parole_nome_cognome = nome_cognome.split('_')
    presente = False

    for parola in parole_nome_cognome:
        if parola.lower() in url.lower():
            presente = True
            break

    if presente:
        corresponding_rows.append(row)
    else:
        non_corresponding_rows.append(row)

corresponding_url_df = pd.DataFrame(corresponding_rows, columns=df_donne_con_url2 .columns)
non_corresponding_url_df = pd.DataFrame(non_corresponding_rows, columns=df_donne_con_url2 .columns)


pd.set_option('display.max_colwidth', None)
print("URL corrispondenti di quelli della ricerca del nome:")
print(corresponding_url_df)
print(len(corresponding_url_df))

print("\nURL non corrispondenti:")
print(non_corresponding_url_df)
print(len(non_corresponding_url_df))


import re
from bs4 import BeautifulSoup
import requests


def check_birth_date_in_url(df):
    def check_birth_date(url, birth_date):
        response = requests.get(url)
        if response.status_code == 200:
            html_code = response.text
            soup = BeautifulSoup(html_code, 'html.parser')
            mw_parser_output = soup.find('div', class_='mw-parser-output')
            if mw_parser_output:
                p_tags = mw_parser_output.find_all('p')
                for p_tag in p_tags:
                    if all(re.search(r'\b{}\b'.format(re.escape(part)), str(p_tag)) for part in birth_date.split(' ')):
                        return True
        return False

    df_with_birthdate = pd.DataFrame(columns=df.columns)
    df_without_birthdate = pd.DataFrame(columns=df.columns)

    for index, row in df.iterrows():
        url = row['URL']
        birth_date = row['Data di nascita']
        corrisponde = check_birth_date(url, birth_date)
        if corrisponde:
            df_with_birthdate = pd.concat([df_with_birthdate, row.to_frame().T])
        else:
            df_without_birthdate = pd.concat([df_without_birthdate, row.to_frame().T])

    return df_with_birthdate, df_without_birthdate

df_with_birthdate, df_without_birthdate = check_birth_date_in_url(corresponding_url_df)

print("DataFrame con corrispondenza di data di nascita:")
print(df_with_birthdate)
print(len(df_with_birthdate))

print("DataFrame senza corrispondenza di data di nascita:")
print(df_without_birthdate)
print(len(df_without_birthdate))

df_with_url = df_with_url.rename(columns={"Nome": "Persona"})
df_controllo_wiki = pd.concat([df_with_url, df_donne_con_url, df_with_birthdate])
print("numero di tutti gli url che ho ottenuto 41")
print(df_controllo_wiki)
print(len(df_controllo_wiki))
print("numero di quelli di cui già non ho info adesso 8 ")
print(len(df_without_birthdate)) #5 più quelli di non_corresponding_urldf

#CONTROLLO CHE NELLE PAGINE DI WIKIPEDIA CI SIA LA SEZIONE TITOLO DI STUDIO
urldaesaminare= df_controllo_wiki["URL"].tolist()
#print(urldaesaminare)
# Inizializza una lista per i dataframe
dataframes = []

# Itera sugli URL
for url in urldaesaminare:
    response = requests.get(url)
    html_content = response.text

    # Analizzare l'HTML con BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Trovare tutti gli elementi <tr>
    tr_elements = soup.find_all("tr")

    # Inizializza le liste per i valori di <th> e <td>
    th_values = []
    td_values = []

    # Scorrere gli elementi <tr> e controllare i valori di <th> e <td>
    for tr_element in tr_elements:
        th_elements = tr_element.find_all("th")
        td_elements = tr_element.find_all("td")

        for th_element in th_elements:
            th_value = th_element.text.strip()
            th_values.append(th_value)

            # Se esiste un elemento <td> associato, aggiungi il suo valore alla lista
            if td_elements:
                td_value = td_elements[0].text.strip()
                td_values.append(td_value)
            else:
                td_values.append("")

    # Crea il dataframe utilizzando le liste di valori
    data = {"th": th_values, "td": td_values, "url": [url] * len(th_values)}
    df = pd.DataFrame(data)

    # Aggiungi il dataframe alla lista
    dataframes.append(df)

# Concatena tutti i dataframe in uno unico
final_df = pd.concat(dataframes, ignore_index=True)

df_filt = final_df[final_df['th'].str.contains('studio')]
df_filt = df_filt.merge(df_controllo_wiki[['URL', 'Persona']], left_on='url', right_on='URL', how='left')
print("Donne con sezione titolo di studio:")
print(len(df_filt))


#CONTROLLO CHE NELLA SEZIONE TITOLO DI STUDIO CI SIA LAUREA O DIPLOMA PER CAPIRE I LAUREATI
# Creazione dei due DataFrame vuoti
df_filt_con_laurea = pd.DataFrame(columns=df_filt.columns)
df_filt_senza_laurea = pd.DataFrame(columns=df_filt.columns)

# Iteration over the filtered DataFrame
for index, row in df_filt.iterrows():
    if 'laurea' in row['td'].lower():
        df_filt_con_laurea = pd.concat([df_filt_con_laurea, row.to_frame().transpose()], ignore_index=True)
    else:
        df_filt_senza_laurea = pd.concat([df_filt_senza_laurea, row.to_frame().transpose()], ignore_index=True)


df_filt_con_laurea = df_filt_con_laurea.assign(gender='female')
#print(df_filt_con_laurea)
df_filt_con_laurea = df_filt_con_laurea[['Persona', 'gender', 'td']]
df_filt_con_laurea = df_filt_con_laurea.rename(columns={"td": "Descrizione"})


df_filt_senza_laurea = df_filt_senza_laurea.assign(gender='female')
df_filt_senza_laurea = df_filt_senza_laurea[['Persona', 'gender']]

print("df_filt_con_laurea 16")
print(len(df_filt_con_laurea))
print("df_filt_senza_laurea 5")
print(len(df_filt_senza_laurea))



urlconsezionetitolodistudio = df_filt["URL"].tolist()

valori_non_comuni = list(set(urldaesaminare) - set(urlconsezionetitolodistudio))
#print(valori_non_comuni)
print("Valori non comuni, ovvero url senza la sezione titolo di studio ")
print(len(valori_non_comuni)) #url senza sezione titolo di studio


#CONTROLLO DEGLI URL SENZA LA SEZIONE TITOLO DI STUDIO SE HANNO INFO LAUREA NELLA BIO

df_senza_parola = pd.DataFrame(columns=["Persona", "URL"])
df_con_parola = pd.DataFrame(columns=["Persona", "URL", "Descrizione"])

for url in valori_non_comuni:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        h2_elements = soup.find_all("h2")

        found = False  # Flag per indicare se è stata trovata la parola "laurea", "laureò" o "laureata"

        for h2 in h2_elements:
            sibling_p = h2.find_next_sibling("p")
            while sibling_p:
                text = sibling_p.get_text()
                match = re.search(r"\b(laurea|laureò|laureata|Laureatosi|laureatosi)\b", text, re.IGNORECASE)
                if match:
                    start = match.end()  # Indice di fine della parola "laurea"
                    end = start + 20  # Prendi i successivi 20 caratteri
                    context = text[match.start():end].strip()
                    persona = df_controllo_wiki.loc[df_controllo_wiki["URL"].str.lower() == url.lower(), "Persona"].values[0]
                    df_con_parola = pd.concat([df_con_parola, pd.DataFrame({"Persona": [persona], "URL": [url], "Descrizione": [context]})], ignore_index=True)
                    found = True
                    break
                sibling_p = sibling_p.find_next_sibling("p")
            if found:
                break

        if not found:
            persona = df_controllo_wiki.loc[df_controllo_wiki["URL"].str.lower() == url.lower(), "Persona"].values[0]
            df_senza_parola = pd.concat([df_senza_parola, pd.DataFrame({"Persona": [persona], "URL": [url]})], ignore_index=True)

    else:
        print(f"Errore nella richiesta della pagina di Wikipedia per l'URL: {url}")

# Aggiungo il genere e le colonne nome, cognome e URL per il dataframe finale
df_con_parola = df_con_parola.assign(gender='female')
df_con_parola = df_con_parola[['Persona', 'gender', 'Descrizione', 'URL']]

df_senza_parola = df_senza_parola.assign(gender='female')
df_senza_parola = df_senza_parola[['Persona', 'gender', 'URL']]

# Stampa dei DataFrame
print("Pagine con almeno una delle parole:")
print(len(df_con_parola))
print(df_con_parola["Descrizione"])

print("Pagine senza nessuna delle parole:")
print(len(df_senza_parola))


#Controllo della professione per quelli che non hanno nè titolo di studio nè parola

listacheckprofessione = df_senza_parola["URL"].tolist()
#print(len(listacheckprofessione))
# Inizializza una lista per i dataframe
dataframes = []

# Itera sugli URL
for url in listacheckprofessione:
    response = requests.get(url)
    html_content = response.text

    # Analizzare l'HTML con BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Trovare tutti gli elementi <tr>
    tr_elements = soup.find_all("tr")

    # Inizializza le liste per i valori di <th> e <td>
    th_values = []
    td_values = []

    # Scorrere gli elementi <tr> e controllare i valori di <th> e <td>
    for tr_element in tr_elements:
        th_elements = tr_element.find_all("th")
        td_elements = tr_element.find_all("td")

        for th_element in th_elements:
            th_value = th_element.text.strip()
            th_values.append(th_value)

            # Se esiste un elemento <td> associato, aggiungi il suo valore alla lista
            if td_elements:
                td_value = td_elements[0].text.strip()
                td_values.append(td_value)
            else:
                td_values.append("")

    # Crea il dataframe utilizzando le liste di valori
    data = {"th": th_values, "td": td_values, "url": [url] * len(th_values)}
    df = pd.DataFrame(data)

    # Aggiungi il dataframe alla lista
    dataframes.append(df)

# Concatena tutti i dataframe in uno unico
print(len(dataframes))
final_df = pd.concat(dataframes, ignore_index=True)
#print(final_df)
#final_df = final_df.drop_duplicates(subset=['url'])
#print(len(final_df))
df_filtprofessione = final_df[final_df['th'].str.contains('Professione')]
df_filtprofessione = df_filtprofessione.merge(df_senza_parola[['URL', 'Persona']], left_on='url', right_on='URL', how='left')
print("URL con sezione professione")
#print(df_filtprofessione)
print(df_filtprofessione)

df_da_escludere = df_filtprofessione[["url"]]
url_senza_professione = final_df[~final_df['url'].isin(df_da_escludere['url'])]
url_senza_professione = url_senza_professione.drop_duplicates(subset=['url'])
url_senza_professione = url_senza_professione.rename(columns={"th": "Persona"})
url_senza_professione = url_senza_professione.rename(columns={'td': 'Descrizione'})

# Unire le parole della colonna "Persona" con "_"
url_senza_professione["Persona"] = url_senza_professione["Persona"].apply(lambda x: "_".join(x.split()))

# Selezionare solo le colonne desiderate nel dataframe "url_senza_professione"
url_senza_professione = url_senza_professione[['Persona']]
#lista3 = list(set(listacheckprofessione) ^ set(listacheck))
#print(df_senzaprofessione)
#print(lista3)
print("url senza professione")
print(len(url_senza_professione))

df_medico = pd.DataFrame(columns=df.columns)
df_altro = pd.DataFrame(columns=df.columns)

for index, row in df_filtprofessione.iterrows():
    professione = row['td'].lower()
    if 'medico' in professione:
        df_medico = pd.concat([df_medico, row.to_frame().transpose()], ignore_index=True)
    else:
        df_altro = pd.concat([df_altro, row.to_frame().transpose()], ignore_index=True)

# Stampa dei tre DataFrame risultanti
print("DataFrame Medico:")
print(len(df_medico))
print(df_medico)
print("DataFrame altro:")
print(len(df_altro))
print(df_altro)

# Estrazione del nome e del cognome dall'URL
df_medico = df_medico.assign(gender='female')
df_medico = df_medico[['Persona', 'gender', 'td']]
df_medico = df_medico.rename(columns={'td': 'Descrizione'})

df_altro = df_altro.assign(gender='female')
df_altro= df_altro[['Persona', 'gender', 'td']]
df_altro = df_altro.rename(columns={'td': 'Descrizione'})
df_con_parola = df_con_parola[['Persona', 'gender', 'Descrizione']]
wikipedia_df = pd.concat([df_filt_con_laurea, df_con_parola, df_medico])
wikipedia_df["Property"] = "dc:description"
wikipedia_df = wikipedia_df[["Persona", "Property", "Descrizione"]]

print("wikipediadf")
print(wikipedia_df)
df_con_parola = df_con_parola[['Persona', 'gender']]
df_donnelaureate_f = pd.concat([df_filt_con_laurea, donnelaureate, df_con_parola, df_medico])
df_donnelaureate_f = df_donnelaureate_f.assign(graduated='yes')
df_donnelaureate_f = df_donnelaureate_f[['Persona', 'gender', 'graduated']]
#print("Donne laureate totale:")
#print(len(df_donnelaureate_f))

df_donnenonlaureate_f = pd.concat([df_filt_senza_laurea, donnenonlaureate, df_altro])
df_donnenonlaureate_f = df_donnenonlaureate_f.assign(graduated='no')
df_donnenonlaureate_f = df_donnenonlaureate_f[['Persona', 'gender', 'graduated']]

df_donne_senza_url  = df_donne_senza_url["Persona e Data di nascita"].apply(lambda x: x[0])
df_donne_senza_url  = pd.DataFrame(df_donne_senza_url , columns=["Persona"])
df_donne_senza_url = df_donne_senza_url.assign(gender='female')
df_without_url = df_without_url[["Nome"]]
df_without_url = df_without_url.rename(columns={'Nome': 'Persona'})
df_donne_senza_info_f = pd.concat([non_corresponding_url_df, df_without_birthdate, url_senza_professione])
df_donne_senza_info_f = df_donne_senza_info_f.assign(gender='female')
df_donne_senza_info_f = df_donne_senza_info_f.assign(graduated='NaN')
df_donne_senza_info_f = df_donne_senza_info_f[["Persona", "gender", "graduated"]]
#print(df_donne_senza_url)
#print("Donne non laureate totale:")
#print(len(df_donnenonlaureate_f))
#print(len(df_donne_senza_info_f))

df_laurea_donne_f = pd.concat([df_donne_senza_info_f, df_donnenonlaureate_f, df_donnelaureate_f])
#print(df_laurea_donne_f)
print(len(df_laurea_donne_f))
#print(len(df_laurea_donne_f))

df_laurea_donne_f.to_csv("graduationfemale.csv",  index=False, index_label=False)
#print(df_filt_senza_laurea)
#print(df_altro)
#print(df_filt_con_laurea)
#print(df_medico)
#print(df_con_parola)
#print(df_with_birthdate)
#print(non_corresponding_url_df)
#print(donnenonlaureate)

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


endpoint = "https://dati.camera.it/sparql"
pd.set_option('display.max_rows', None)

querydefinitivalaureauomini ="""SELECT DISTINCT ?persona ?cognome ?nome ?info
?dataNascita ?luogoNascita
WHERE {
?persona ocd:rif_mandatoCamera ?mandato; a foaf:Person.

?d a ocd:deputato;
ocd:rif_leg ?legislatura;
ocd:rif_mandatoCamera ?mandato.
OPTIONAL{?d dc:description ?info}

##anagrafica
?d foaf:surname ?cognome; foaf:gender "male" ;foaf:firstName ?nome.
OPTIONAL{
?persona <http://purl.org/vocab/bio/0.1/Birth> ?nascita.
?nascita <http://purl.org/vocab/bio/0.1/date> ?dataNascita;
rdfs:label ?nato; ocd:rif_luogo ?luogoNascitaUri.
?luogoNascitaUri dc:title ?luogoNascita.
}}"""
df_laurea_uomini = get(endpoint, querydefinitivalaureauomini)
df_laurea_uomini = df_laurea_uomini.drop_duplicates(["persona","nome", "cognome", "luogoNascita"]) #5204
df_laurea_uomini_data = df_laurea_uomini.drop_duplicates(["persona","nome", "cognome", "dataNascita","luogoNascita"])
df_uomini_noinfo = df_laurea_uomini[df_laurea_uomini['info'].isna()]
df_uomini_noinfo_data = df_uomini_noinfo[["nome", "cognome", "dataNascita"]]
#print(len(df_laurea_uomini_data))
#df_laurea_uomini = df_laurea_uomini.sort_values(by='cognome')

import locale
from datetime import datetime

#Modifica della formattazione dei nomi per permettere la ricerca degli URL wikipedia
os.environ['LC_TIME'] = 'it_IT.UTF-8'

mesi_italiani = {
    'January': 'gennaio',
    'February': 'febbraio',
    'March': 'marzo',
    'April': 'aprile',
    'May': 'maggio',
    'June': 'giugno',
    'July': 'luglio',
    'August': 'agosto',
    'September': 'settembre',
    'October': 'ottobre',
    'November': 'novembre',
    'December': 'dicembre'
}

lista_politici_data_nascita = []

def capitalize_name(name):
    parts = re.split(r"([ '-])", name)
    return "".join([part.capitalize() for part in parts])

for index, row in df_uomini_noinfo_data.iterrows():
    nome = row['nome'].split()
    cognome = row['cognome'].split()
    nome_cognome = "_".join([capitalize_name(word) for word in nome + cognome])
    data_nascita = row['dataNascita']
    if pd.notna(data_nascita):
        data = datetime.strptime(str(int(data_nascita)), "%Y%m%d")
        giorno = str(data.day)  # Converte il giorno in stringa
        mese_in_inglese = data.strftime("%B")
        mese = mesi_italiani.get(mese_in_inglese, mese_in_inglese)
        anno = str(data.year)  # Converte l'anno in stringa
        data_formattata = f"{giorno} {mese} {anno}"
        lista_politici_data_nascita.append((nome_cognome, data_formattata))
    else:
        lista_politici_data_nascita.append((nome_cognome, ""))

#print(lista_politici_data_nascita)


df_laurea_uomini['info'] = df_laurea_uomini['info'].fillna('')
masklaurea = df_laurea_uomini['info'].str.contains('Laurea|laurea|Master|LAUREA')

# Estrazione delle persone che hanno laurea dai dati di dati camera
laureati = df_laurea_uomini[masklaurea]
laureati = laureati.assign(gender='male')
uominilaureati = laureati[["nome", "cognome", "gender"]]
def capitalize_name(name):
    parts = re.findall(r"[\w'-]+", name)
    capitalized_parts = [part.capitalize() for part in parts]
    return "_".join(capitalized_parts)

for index, row in uominilaureati.iterrows():
    nome = row['nome']
    cognome = row['cognome']
    persona = capitalize_name(nome) + "_" + capitalize_name(cognome)
    uominilaureati.at[index, 'Persona'] = persona

# Seleziona solo le colonne desiderate
uominilaureati = uominilaureati[['Persona', 'gender']]
#print(uominilaureati)

masknonlaurea =~df_laurea_uomini['info'].str.contains('Laurea|laurea|Master|LAUREA', na=False) & df_laurea_uomini['info'].ne('')
uomininonlaureati = df_laurea_uomini[masknonlaurea]
#uomininonlaureati = uomininonlaureati.assign(info="no")
uomininonlaureati = uomininonlaureati.assign(gender='male')
uomininonlaureati = uomininonlaureati[["nome","cognome", "gender"]]



def capitalize_name(name):
    parts = re.findall(r"[\w'-]+", name)
    capitalized_parts = [part.capitalize() for part in parts]
    return "_".join(capitalized_parts)

for index, row in uomininonlaureati.iterrows():
    nome = row['nome']
    cognome = row['cognome']
    persona = capitalize_name(nome) + "_" + capitalize_name(cognome)
    uomininonlaureati.at[index, 'Persona'] = persona

# Seleziona solo le colonne desiderate
uomininonlaureati = uomininonlaureati[['Persona', 'gender']]
#print(uomininonlaureati)

print("UOMINI TOTALE 5204")
print(len(df_laurea_uomini)) #5204
print("UOMINI LAUREATI 3293")
print(len(uominilaureati)) #3293
print("UOMINI NO INFO 162")
print(len(df_uomini_noinfo)) #162
print("UOMINI NON LAUREATI 1749")
#print(uomininonlaureati) #1749
print(len(uomininonlaureati))


#CERCA PAGINA WIKIPEDIA DELLE PERSONE SENZA INFORMAZIONI SUL TITOLO DI STUDIO

import re
from bs4 import BeautifulSoup

def check_url_exists(url):
    response = requests.get(url)
    return response.status_code == 200

def extract_birth_date(text):
    if '–' in text:
        date_range = re.findall(r'(\d+\s\w+\s\d+)', text)
        if date_range:
            birth_date = date_range[0]
            if birth_date in text.split('–')[0]:
                return birth_date
    else:
        matches = re.findall(r'(\d+\s\w+\s\d+)', text)
        if matches:
            return matches[0]
    return None

url_lista = []
uomini_con_url = []
uomini_senza_url = []

for nome_cognome, data_nascita in lista_politici_data_nascita:
    url_politico_data = None
    for anno_iniziale in [1952, 1940, 1929]:
        url_politico_data = f"https://it.wikipedia.org/wiki/{nome_cognome}_(politico_{anno_iniziale})"
        if check_url_exists(url_politico_data):
            pagina_wikipedia = requests.get(url_politico_data)
            if pagina_wikipedia.status_code == 200:
                soup = BeautifulSoup(pagina_wikipedia.text, 'html.parser')
                paragraph = soup.find('p')
                if paragraph:
                    birth_date = extract_birth_date(paragraph.text)
                    if birth_date and (birth_date == data_nascita or birth_date.split(' – ')[0] == data_nascita):
                        #print(f"URL della pagina di Wikipedia per {nome_cognome} (politico con data): {url_politico_data}")
                        url_lista.append(url_politico_data)
                        uomini_con_url.append(nome_cognome)
                        break
                else:
                    print("Paragrafo non trovato.")
    else:
        url_politico = f"https://it.wikipedia.org/wiki/{nome_cognome}_(politico)"
        url_generale = f"https://it.wikipedia.org/wiki/{nome_cognome}"
        if check_url_exists(url_politico):
            pagina_wikipedia = requests.get(url_politico)
            if pagina_wikipedia.status_code == 200:
                soup = BeautifulSoup(pagina_wikipedia.text, 'html.parser')
                paragraph = soup.find('p')
                if paragraph:
                    birth_date = extract_birth_date(paragraph.text)
                    if birth_date and (birth_date == data_nascita or birth_date.split(' – ')[0] == data_nascita):
                        #print(f"URL della pagina di Wikipedia per {nome_cognome} (politico): {url_politico}")
                        url_lista.append(url_politico)
                        uomini_con_url.append(nome_cognome)
                        continue
                else:
                    print("Paragrafo non trovato.")
        if check_url_exists(url_generale):
            pagina_wikipedia = requests.get(url_generale)
            if pagina_wikipedia.status_code == 200:
                soup = BeautifulSoup(pagina_wikipedia.text, 'html.parser')
                paragraph = soup.find('p')
                if paragraph:
                    birth_date = extract_birth_date(paragraph.text)
                    if birth_date and (birth_date == data_nascita or birth_date.split(' – ')[0] == data_nascita):
                        #print(f"URL della pagina di Wikipedia generica per {nome_cognome}: {url_generale}")
                        url_lista.append(url_generale)
                        uomini_con_url.append(nome_cognome)
                        continue
                else:
                    print("Paragrafo non trovato.")
        print(f"Nessun URL trovato per {nome_cognome}")

        uomini_senza_url.append((nome_cognome, data_nascita))


df_uomini_con_url = pd.DataFrame({"Persona": uomini_con_url, "URL": url_lista})
for index, row in df_uomini_con_url.iterrows():
    persona = row["Persona"]
    for nome_cognome, data_nascita in lista_politici_data_nascita:
        if nome_cognome == persona:
            df_uomini_con_url.at[index, "Data di nascita"] = data_nascita
            break

df_uomini_senza_url = pd.DataFrame({"Persona e Data di nascita": uomini_senza_url})
pd.set_option('display.max_colwidth', None)
print("Uomini che hanno url subito 111")
#print(df_uomini_con_url)
print(df_uomini_con_url)
print("Uomini senza url subito 51")
print(len(df_uomini_senza_url))

lista_uomini_senza_url = df_uomini_senza_url['Persona e Data di nascita'].values.tolist()

import pandas as pd
import wikipediaapi
import re

#Stesso controllo ma per vedere le date primo e per quelli che sono morti e quindi hanno due date su cui fare il check ecc

def extract_birth_date(text):
    if '–' in text:
        date_range = re.findall(r'(\d+\s\w+\s\d+)', text)
        if date_range:
            birth_date = date_range[0]
            if birth_date in text.split('–')[0]:
                return birth_date
    else:
        matches = re.findall(r'(\d+º?\s\w+\s\d+)', text)
        if matches:
            birth_date = matches[0]
            if birth_date.startswith('1º'):
                return birth_date.replace('º', '')
            return birth_date

def find_wikipedia_url(nome_cognome, data_nascita):
    headers = {
        'User-Agent': 'My Wikipedia Script (elizastuglik@gmail.com)'
    }

    wiki_wiki = wikipediaapi.Wikipedia("it", headers=headers)
    url_politico_data = None
    url_politico = None
    url_generale = None

    for anno_iniziale in [1952, 1940, 1929]:
        page_name = f"{nome_cognome} (politico {anno_iniziale})"
        page = wiki_wiki.page(page_name)
        if page.exists():
            content = page.text
            birth_date = extract_birth_date(content)
            if birth_date and (birth_date == data_nascita or birth_date.split(' – ')[0] == data_nascita):
                url_politico_data = page.fullurl
                break

    if not url_politico_data:
        page_name = f"{nome_cognome} (politico)"
        page = wiki_wiki.page(page_name)
        if page.exists():
            content = page.text
            birth_date = extract_birth_date(content)
            if birth_date and (birth_date == data_nascita or birth_date.split(' – ')[0] == data_nascita):
                url_politico = page.fullurl

    if not url_politico_data and not url_politico:
        page_name = nome_cognome
        page = wiki_wiki.page(page_name)
        if page.exists():
            content = page.text
            birth_date = extract_birth_date(content)
            if birth_date and (birth_date == data_nascita or birth_date.split(' – ')[0] == data_nascita):
                url_generale = page.fullurl

    if url_politico_data:
        return (nome_cognome, data_nascita, url_politico_data)
    elif url_politico:
        return (nome_cognome, data_nascita, url_politico)
    elif url_generale:
        return (nome_cognome, data_nascita, url_generale)
    else:
        return (nome_cognome, data_nascita, None)

df_with_url = pd.DataFrame(columns=['Nome', 'Data di nascita', 'URL'])
df_without_url = pd.DataFrame(columns=['Nome', 'Data di nascita'])

for item in lista_uomini_senza_url:
    nome_cognome, data_nascita, url = find_wikipedia_url(item[0], item[1])
    if url:
        df_with_url = pd.concat([df_with_url, pd.DataFrame({'Nome': [nome_cognome], 'Data di nascita': [data_nascita], 'URL': [url]})], ignore_index=True)
    else:
        df_without_url = pd.concat([df_without_url, pd.DataFrame({'Nome': [nome_cognome], 'Data di nascita': [data_nascita]})], ignore_index=True)

pd.set_option('display.max_colwidth', None)

print("UOMINI CON URL DOPO IL PRIMO TENT 15:")
#print(df_with_url)
print(len(df_with_url))
print("UOMINI SENZA URL ANCHE DOPO QUESTO TENT 36:")
#print(df_without_url)
print(len(df_without_url))


#Trovare quelli che hanno dei secondi nomi su wiki ecc

# Funzione per controllare l'esistenza dell'URL
def check_url_exists(url):
    response = requests.get(url)
    return response.status_code == 200

# Funzione per ottenere URL alternativi
def get_alternative_urls(nome, cognome):
    search_query = f"https://it.wikipedia.org/w/index.php?title=Speciale:Search&search={nome}+{cognome}"
    search_response = requests.get(search_query)

    alternative_urls = []

    if search_response.status_code == 200:
        search_soup = BeautifulSoup(search_response.content, "html.parser")
        search_results = search_soup.find_all("div", class_="mw-search-result-heading")

        for result in search_results:
            result_link = result.find("a")
            result_url = result_link["href"]
            url = f"https://it.wikipedia.org{result_url}"
            decoded_url = urllib.parse.unquote(url)  # Decodifica l'URL per visualizzare i caratteri speciali
            alternative_urls.append(decoded_url)

    return alternative_urls

url_lista = []
uomini_con_url2 = []
uomini_senza_url2 = []
date_nascita_senza_url2 = []
date_nascita_con_url2 = []

for index, row in df_without_url.iterrows():
    persona = row['Nome']
    nome_cognome_parts = persona.split("_")
    nome = nome_cognome_parts[0]
    cognome = nome_cognome_parts[-1]

    response = requests.get(f"https://it.wikipedia.org/wiki/{persona}", timeout=10)

    if response.status_code == 200:
        url_lista.append(response.url)
        uomini_con_url2.append(persona)
        date_nascita_con_url2.append(row['Data di nascita'])
    else:
        alternative_urls = get_alternative_urls(nome, cognome)

        for alternative_url in alternative_urls:
            if check_url_exists(alternative_url):
                url_lista.append(alternative_url)
                uomini_con_url2.append(persona)
                date_nascita_con_url2.append(row['Data di nascita'])
                break
        else:
            uomini_senza_url2.append(persona)
            date_nascita_senza_url2.append(row['Data di nascita'])

df_uomini_con_url2 = pd.DataFrame({"Persona": uomini_con_url2, "URL": url_lista, "Data di nascita": date_nascita_con_url2})
df_uomini_senza_url2 = pd.DataFrame({"Persona": uomini_senza_url2, "Data di nascita": date_nascita_senza_url2})

print("Lunghezza dataframe uomini con URL 34:")
#print(df_uomini_con_url2)
print(len(df_uomini_con_url2))
print("Lunghezza dataframe uomini senza URL 2:")
#print(df_uomini_senza_url2)
print(len(df_uomini_senza_url2))

#Controlliamo se nell'url c'è effettivamente il nome o il cognome
corresponding_rows = []
non_corresponding_rows = []

for _, row in df_uomini_con_url2 .iterrows():
    nome_cognome = row['Persona']
    url = row['URL']

    parole_nome_cognome = nome_cognome.split('_')
    presente = False

    for parola in parole_nome_cognome:
        if parola.lower() in url.lower():
            presente = True
            break

    if presente:
        corresponding_rows.append(row)
    else:
        non_corresponding_rows.append(row)

corresponding_url_df = pd.DataFrame(corresponding_rows, columns=df_uomini_con_url2 .columns)
non_corresponding_url_df = pd.DataFrame(non_corresponding_rows, columns=df_uomini_con_url2 .columns)

pd.set_option('display.max_colwidth', None)

print("URL corrispondenti 23:")
#print(corresponding_url_df)
print(len(corresponding_url_df))

print("\nURL non corrispondenti 11:")
print(non_corresponding_url_df)

import re
from bs4 import BeautifulSoup
import requests

def check_birth_date_in_url(df):
    def check_birth_date(url, birth_date):
        response = requests.get(url)
        if response.status_code == 200:
            html_code = response.text
            soup = BeautifulSoup(html_code, 'html.parser')
            mw_parser_output = soup.find('div', class_='mw-parser-output')
            if mw_parser_output:
                p_tags = mw_parser_output.find_all('p')
                for p_tag in p_tags:
                    if all(re.search(r'\b{}\b'.format(re.escape(part)), str(p_tag)) for part in birth_date.split(' ')):
                        return True
        return False

    df_with_birthdate = pd.DataFrame(columns=df.columns)
    df_without_birthdate = pd.DataFrame(columns=df.columns)

    for index, row in df.iterrows():
        url = row['URL']
        birth_date = row['Data di nascita']
        corrisponde = check_birth_date(url, birth_date)
        if corrisponde:
            df_with_birthdate = pd.concat([df_with_birthdate, pd.DataFrame(row).transpose()], ignore_index=True)
        else:
            df_without_birthdate = pd.concat([df_without_birthdate, pd.DataFrame(row).transpose()], ignore_index=True)

    return df_with_birthdate, df_without_birthdate

df_with_birthdate, df_without_birthdate = check_birth_date_in_url(corresponding_url_df)

print("DataFrame con corrispondenza di data di nascita:")
#print(df_with_birthdate)
print(len(df_with_birthdate))

print("DataFrame senza corrispondenza di data di nascita:")
#print(df_without_birthdate)
print(len(df_without_birthdate))

df_with_url = df_with_url.rename(columns={"Nome": "Persona"})
pd.set_option('display.max_colwidth', None)
#print("URL trovati dopo check secondo nome 3")
#print(len(df_with_url2))
# Stampa il dataframe risultante
#print(df_with_birth_date)
#print(df_with_url.columns)
#print(df_with_url2.columns)
#print(df_uomini_con_url.columns)
#UNISCO TUTTI I DATAFRAME CON GLI URL DI WIKIPEDIA DA CONTROLLARE

df_controllo_wiki = pd.concat([df_with_url, df_uomini_con_url, df_with_birthdate])

print("numero di tutti gli url che ho ottenuto")
#print(df_controllo_wiki)
print(len(df_controllo_wiki))
#print(df_controllo_wiki)

#CONTROLLO CHE NELLE PAGINE DI WIKIPEDIA CI SIA LA SEZIONE TITOLO DI STUDIO
urldaesaminare= df_controllo_wiki["URL"].tolist()
#print(urldaesaminare)
# Inizializza una lista per i dataframe
dataframes = []

# Itera sugli URL
for url in urldaesaminare:
    response = requests.get(url)
    html_content = response.text

    # Analizzare l'HTML con BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Trovare tutti gli elementi <tr>
    tr_elements = soup.find_all("tr")

    # Inizializza le liste per i valori di <th> e <td>
    th_values = []
    td_values = []

    # Scorrere gli elementi <tr> e controllare i valori di <th> e <td>
    for tr_element in tr_elements:
        th_elements = tr_element.find_all("th")
        td_elements = tr_element.find_all("td")

        for th_element in th_elements:
            th_value = th_element.text.strip()
            th_values.append(th_value)

            # Se esiste un elemento <td> associato, aggiungi il suo valore alla lista
            if td_elements:
                td_value = td_elements[0].text.strip()
                td_values.append(td_value)
            else:
                td_values.append("")

    # Crea il dataframe utilizzando le liste di valori
    data = {"th": th_values, "td": td_values, "url": [url] * len(th_values)}
    df = pd.DataFrame(data)

    # Aggiungi il dataframe alla lista
    dataframes.append(df)

# Concatena tutti i dataframe in uno unico
final_df = pd.concat(dataframes, ignore_index=True)


df_filt = final_df[final_df['th'].str.contains('studio')]
#print(len(df_filt))
df_filt = df_filt.merge(df_controllo_wiki[['URL', 'Persona']], left_on='url', right_on='URL', how='left')
print("df_filt")
print(len(df_filt))
#print(df_filt)
#df_filt = df_filt.drop('url', axis=1)
#print(df_filt)
#CONTROLLO CHE NELLA SEZIONE TITOLO DI STUDIO CI SIA LAUREA O DIPLOMA PER CAPIRE I LAUREATI

# Creazione dei due DataFrame vuoti
df_filt_con_laurea = pd.DataFrame(columns=df_filt.columns)
df_filt_senza_laurea = pd.DataFrame(columns=df_filt.columns)

# Iteration over the filtered DataFrame
for index, row in df_filt.iterrows():
    if 'laurea' in row['td'].lower():
        df_filt_con_laurea = pd.concat([df_filt_con_laurea, row.to_frame().transpose()], ignore_index=True)
    else:
        df_filt_senza_laurea = pd.concat([df_filt_senza_laurea, row.to_frame().transpose()], ignore_index=True)
#print("df filt con laurea")
#print(df_filt_con_laurea)


df_filt_con_laurea = df_filt_con_laurea.assign(gender='male')
df_filt_con_laurea = df_filt_con_laurea[['Persona', 'gender', 'td']]
df_filt_con_laurea = df_filt_con_laurea.rename(columns={"td": "Descrizione"})


df_filt_senza_laurea = df_filt_senza_laurea.assign(gender='male')
df_filt_senza_laurea = df_filt_senza_laurea[['Persona', 'gender']]

print("df_filt_con_laurea")
print(len(df_filt_con_laurea))
print("df_filt_senza_laurea")
print(len(df_filt_senza_laurea))

urlconsezionetitolodistudio = df_filt["URL"].tolist()
#print(len(urlconsezionetitolodistudio))
valori_non_comuni = list(set(urldaesaminare) - set(urlconsezionetitolodistudio))
#print(valori_non_comuni)
print("Valori non comuni, ovvero url senza la sezione titolo di studio ")
print(len(valori_non_comuni)) #url senza sezione titolo di studio   67
#print(valori_non_comuni)
#print(df_filt)

#CONTROLLO DEGLI URL SENZA LA SEZIONE TITOLO DI STUDIO SE HANNO INFO LAUREA NELLA BIO


df_con_parola = pd.DataFrame(columns=["Persona", "URL", "Descrizione"])
df_senza_parola = pd.DataFrame(columns=["Persona", "URL"])

for url in valori_non_comuni:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        h2_elements = soup.find_all("h2")

        found = False  # Flag per indicare se è stata trovata la parola "laurea", "laureò" o "laureata"

        for h2 in h2_elements:
            sibling_p = h2.find_next_sibling("p")
            while sibling_p:
                text = sibling_p.get_text()
                match = re.search(r"\b(laurea|laureò|laureato|Laureatosi|laureatosi)\b", text, re.IGNORECASE)
                if match:
                    start = match.end()  # Indice di fine della parola "laurea"
                    end = start + 20  # Prendi i successivi 20 caratteri
                    context = text[match.start():end].strip()
                    persona = df_controllo_wiki.loc[df_controllo_wiki["URL"].str.lower() == url.lower(), "Persona"].values[0]
                    df_con_parola = pd.concat([df_con_parola, pd.DataFrame({"Persona": [persona], "URL": [url], "Descrizione": [context]})], ignore_index=True)
                    found = True
                    break
                sibling_p = sibling_p.find_next_sibling("p")
            if found:
                break

        if not found:
            persona = df_controllo_wiki.loc[df_controllo_wiki["URL"].str.lower() == url.lower(), "Persona"].values[0]
            df_senza_parola = pd.concat([df_senza_parola, pd.DataFrame({"Persona": [persona], "URL": [url]})], ignore_index=True)

    else:
        print(f"Errore nella richiesta della pagina di Wikipedia per l'URL: {url}")

df_con_parola = df_con_parola.assign(gender='male')
df_con_parola = df_con_parola[['Persona', 'gender', 'Descrizione','URL']]

df_senza_parola = df_senza_parola.assign(gender='male')
df_senza_parola = df_senza_parola[['Persona', 'gender', 'URL']]

# Stampa dei DataFrame

print("Pagine con almeno una delle parole:")
print(df_con_parola["Descrizione"])
print(len(df_con_parola))

print("Pagine senza nessuna delle parole:")
print(df_senza_parola)
print(len(df_senza_parola))


#Controllo della professione per quelli che non hanno nè titolo di studio nè parola

listacheckprofessione = df_senza_parola["URL"].tolist()
#print(len(listacheckprofessione))
# Inizializza una lista per i dataframe
dataframes = []

# Itera sugli URL
for url in listacheckprofessione:
    response = requests.get(url)
    html_content = response.text

    # Analizzare l'HTML con BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Trovare tutti gli elementi <tr>
    tr_elements = soup.find_all("tr")

    # Inizializza le liste per i valori di <th> e <td>
    th_values = []
    td_values = []

    # Scorrere gli elementi <tr> e controllare i valori di <th> e <td>
    for tr_element in tr_elements:
        th_elements = tr_element.find_all("th")
        td_elements = tr_element.find_all("td")

        for th_element in th_elements:
            th_value = th_element.text.strip()
            th_values.append(th_value)

            # Se esiste un elemento <td> associato, aggiungi il suo valore alla lista
            if td_elements:
                td_value = td_elements[0].text.strip()
                td_values.append(td_value)
            else:
                td_values.append("")

    # Crea il dataframe utilizzando le liste di valori
    data = {"th": th_values, "td": td_values, "url": [url] * len(th_values)}
    df = pd.DataFrame(data)

    # Aggiungi il dataframe alla lista
    dataframes.append(df)

# Concatena tutti i dataframe in uno unico
final_df = pd.concat(dataframes, ignore_index=True)
#print(final_df)
#final_df = final_df.drop_duplicates(subset=['url'])
#print(len(final_df))
df_filtprofessione = final_df[final_df['th'].str.contains('Professione')]

df_filtprofessione = df_filtprofessione.merge(df_senza_parola[['URL', 'Persona']], left_on='url', right_on='URL', how='left')
print("URL con sezione professione")
print(len(df_filtprofessione))

df_da_escludere = df_filtprofessione[["url"]]
url_senza_professione = final_df[~final_df['url'].isin(df_da_escludere['url'])]
url_senza_professione = url_senza_professione.drop_duplicates(subset=['url'])
url_senza_professione = url_senza_professione.rename(columns={"th": "Persona"})
url_senza_professione = url_senza_professione.rename(columns={'td': 'Descrizione'})

# Unire le parole della colonna "Persona" con "_"
url_senza_professione["Persona"] = url_senza_professione["Persona"].apply(lambda x: "_".join(x.split()))

# Selezionare solo le colonne desiderate nel dataframe "url_senza_professione"
url_senza_professione = url_senza_professione[['Persona']]
print("url senza professione")
print(len(url_senza_professione))


df_avvocato_professore = pd.DataFrame(columns=df.columns)
df_ingegnere = pd.DataFrame(columns=df.columns)
df_altro = pd.DataFrame(columns=df.columns)

# Iteration over the original DataFrame
for index, row in df_filtprofessione.iterrows():
    professione = row['td'].lower()
    if 'avvocato' in professione or 'docente universitario' in professione:
        df_avvocato_professore = pd.concat([df_avvocato_professore, row.to_frame().transpose()], ignore_index=True)
    elif 'ingegnere' in professione:
        df_ingegnere = pd.concat([df_ingegnere, row.to_frame().transpose()], ignore_index=True)
    else:
        df_altro = pd.concat([df_altro, row.to_frame().transpose()], ignore_index=True)

# Stampa dei tre DataFrame risultanti
print("DataFrame Avvocato/Professore Universitario:")
print(len(df_avvocato_professore))
#print(df_avvocato_professore)
print("DataFrame altro:")
print(len(df_altro))
#print(df_altro)

# Estrazione del nome e del cognome dall'URL

df_avvocato_professore = df_avvocato_professore.assign(gender='male')
df_avvocato_professore = df_avvocato_professore[['Persona', 'gender', 'td']]
df_avvocato_professore = df_avvocato_professore.rename(columns={'td': 'Descrizione'})

#print(df_avvocato_professore)
print("DataFrame Ingegnere:")

df_ingegnere= df_ingegnere[['Persona', 'td']]
df_ingegnere = df_ingegnere.assign(gender='male')
df_ingegnere = df_ingegnere.rename(columns={'td': 'Descrizione'})
print(len(df_ingegnere))
print(df_ingegnere)


#df_altro['nome'] = df_altro['nome'].str.split().str[0]
df_altro = df_altro.assign(gender='male')
df_altro= df_altro[['Persona', 'gender', 'td']]
df_altro = df_altro.rename(columns={'td': 'Descrizione'})
df_con_parola = df_con_parola[['Persona', 'gender', 'Descrizione']]

wikipedia_df = pd.concat([df_filt_con_laurea, df_con_parola, df_ingegnere, df_avvocato_professore])
wikipedia_df["Property"] = "dc:description"
wikipedia_df = wikipedia_df[["Persona", "Property", "Descrizione"]]

print("wikipediadf")
print(wikipedia_df)
df_con_parola = df_con_parola[['Persona', 'gender']]

df_uominilaureati_f = pd.concat([df_filt_con_laurea, uominilaureati, df_con_parola, df_avvocato_professore, df_ingegnere])
df_uominilaureati_f = df_uominilaureati_f.assign(graduated='yes')
df_uominilaureati_f = df_uominilaureati_f[['Persona', 'gender', 'graduated']]
#print("Uomini laureati totale:")
#print(df_uominilaureati_f)
#print(len(df_uominilaureati_f))
df_uomininonlaureati_f = pd.concat([df_filt_senza_laurea,uomininonlaureati, df_altro])
df_uomininonlaureati_f = df_uomininonlaureati_f.assign(graduated='no')
df_uomini_senza_url  = df_uomini_senza_url["Persona e Data di nascita"].apply(lambda x: x[0])
df_uomini_senza_url  = pd.DataFrame(df_uomini_senza_url , columns=["Persona"])
df_uomini_senza_url = df_uomini_senza_url.assign(gender='male')
df_without_url = df_without_url[["Nome"]]
df_without_url = df_without_url.rename(columns={'Nome': 'Persona'})
df_without_birthdate = df_without_birthdate[["Persona"]]
non_corresponding_url_df = non_corresponding_url_df[["Persona"]]
df_uomini_senza_info_f = pd.concat([df_uomini_senza_url2, df_without_birthdate, non_corresponding_url_df, url_senza_professione])
df_uomini_senza_info_f = df_uomini_senza_info_f.assign(gender='male')
df_uomini_senza_info_f = df_uomini_senza_info_f.assign(graduated='NaN')
df_uomini_senza_info_f = df_uomini_senza_info_f[["Persona", "gender", "graduated"]]

df_laurea_uomini_f = pd.concat([df_uomini_senza_info_f, df_uomininonlaureati_f, df_uominilaureati_f])

#print(len(df_laurea_uomini_f))
df_laurea_uomini_f.to_csv("graduation.csv",  index=False, index_label=False)
#print(df_laurea_uomini.columns)
del os.environ['LC_TIME']

# Carica i file CSV
df1 = pd.read_csv('graduation.csv')
df2 = pd.read_csv('graduationfemale.csv')

# Unisci i due dataframe
merged_df = pd.concat([df1, df2], ignore_index=True)

# Salva il risultato in un nuovo file CSV
merged_df.to_csv('mergedgraduationtot.csv', index=False)
