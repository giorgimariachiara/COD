import pandas as pd
import plotly.graph_objects as go

# Read the CSV dataset using Pandas
data = pd.read_csv('graduatedMA.csv')

# Definisci un dizionario che mappa le etichette di legislatura con il corrispondente numero
legislature_mapping = {
    'legislaturaCostituente': 0,
    'legislatura01': 1,
    'legislatura02': 2,
    'legislatura03': 3,
    'legislatura04': 4,
    'legislatura05': 5,
    'legislatura06': 6,
    'legislatura07': 7,
    'legislatura08': 8,
    'legislatura09': 9,
    'legislatura10': 10,
    'legislatura11': 11,
    'legislatura12': 12,
    'legislatura13': 13,
    'legislatura14': 14,
    'legislatura15': 15,
    'legislatura16': 16,
    'legislatura17': 17,
    'legislatura18': 18,
    'legislatura19': 19
}

# Definisci una funzione per ottenere il numero della legislatura da una stringa
def get_legislature_number(legislature_str):
    return legislature_mapping[legislature_str]

# Aggiungi una nuova colonna "legislature_number" con i numeri di legislatura
data['legislature_number'] = data['legislatura'].apply(get_legislature_number)

# Ordina i dati in base al numero di legislatura
data = data.sort_values(by='legislature_number')

# Calcola il numero totale di deputati per ogni legislatura
legislature_counts = data['legislatura'].value_counts()

# Calcola il numero di deputati laureati e non laureati per ogni legislatura
graduated_counts = data[data['graduated'] == 'yes']['legislatura'].value_counts()
non_graduated_counts = legislature_counts - graduated_counts

# Calcola la percentuale di deputati laureati per ogni legislatura
percentage_graduated = (graduated_counts / legislature_counts) * 100

# Crea il grafico Mekko usando Plotly
fig = go.Figure(data=[
    go.Bar(
        x=graduated_counts.index,
        y=graduated_counts.values,
        name='Graduated',
        marker=dict(color='green'),
        text=percentage_graduated.values.round(2),
        textposition='auto',
        texttemplate='%{text:.2f}%',
        hovertemplate='%{y} Graduated<br>%{text} of Total<br>',
    ),
    go.Bar(
        x=non_graduated_counts.index,
        y=non_graduated_counts.values,
        name='Non-Graduated',
        marker=dict(color='purple'),
        hovertemplate='%{y} Non-Graduated<br>',
    )
])

# Personalizza il layout del grafico
fig.update_layout(
    title='Proportion of Graduated and Non-Graduated Deputies by Legislature',
    xaxis=dict(title='Legislature'),
    yaxis=dict(title='Number of Deputies'),
    barmode='stack',
    legend=dict(title='Status'),
)

# Mostra il grafico
fig.show()
