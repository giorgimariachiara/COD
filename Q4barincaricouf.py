import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Lista delle legislature
legislatures_list = ['Costituente', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']

# Lista degli incarichi
labels = ['CAPOGRUPPO', 'SEGRETARIO', 'PRESIDENTE', 'VICEPRESIDENTE', 'RELATORE', 'QUESTORE', 'DELEGATO ALLA PRESIDENZA']


df_female = pd.read_csv('incaricoFEMALE.csv')
df_male = pd.read_csv('incaricoMALE.csv')

app = dash.Dash(__name__)

# Definisci i valori possibili per il filtro dinamico a tendina
legislatures_list = ['Costituente', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']

# Layout dell'applicazione
app.layout = html.Div([
    html.H1("Confronto tra Maschi e Femmine per Legislatori e Incarichi"),
    dcc.Dropdown(
        id='legislatura-dropdown',
        options=[{'label': legislatura, 'value': legislatura} for legislatura in legislatures_list],
        value='Costituente'  # Valore predefinito
    ),
    dcc.Graph(id='bar-chart')
])

# Callback per aggiornare il grafico in base alla selezione del filtro dinamico
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('legislatura-dropdown', 'value')]
)
def update_chart(selected_legislatura):
    # Filtra i dati in base alla legislatura selezionata
    df_female_filtered = df_female[df_female['legislatura'] == selected_legislatura]
    df_male_filtered = df_male[df_male['legislatura'] == selected_legislatura]

    # Calcola il conteggio degli incarichi per maschi e femmine
    counts_female = df_female_filtered['incarico'].value_counts()
    counts_male = df_male_filtered['incarico'].value_counts()

    # Crea il grafico a barre interattivo
    fig = go.Figure()
    fig.add_trace(go.Bar(x=counts_female.index, y=counts_female.values, name='Femmine', marker_color='pink'))
    fig.add_trace(go.Bar(x=counts_male.index, y=counts_male.values, name='Maschi', marker_color='blue'))

    fig.update_layout(
        title=f'Confronto tra Maschi e Femmine per Incarichi - Legislatura {selected_legislatura}',
        xaxis_title='Incarichi',
        yaxis_title='Numero di Persone',
        barmode='group'
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
