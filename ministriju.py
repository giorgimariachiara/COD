
import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Leggi il file CSV
df = pd.read_csv('/content/ministre.csv')  # Assicurati di utilizzare il percorso corretto del file

# Rimuovi le colonne 'nome' e 'cognome'
df = df.drop(columns=['nome', 'cognome'])

# Crea l'applicazione Dash
app = dash.Dash(__name__)

# Ottieni la lista delle legislature presenti nel CSV
legislature_list = sorted(df['legislatura'].unique())

# Layout dell'applicazione
app.layout = html.Div([
    html.H1("Tabella Interattiva delle Legislature"),
    dcc.Dropdown(
        id='legislatura-dropdown',
        options=[{'label': f'Legislatura {l}', 'value': l} for l in legislature_list],
        value=legislature_list[0],
        style={'width': '50%'}
    ),
    dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        style_table={'overflowX': 'auto'},
        style_header={
            'backgroundColor': '#f5f5f5',
            'fontWeight': 'bold'
        },
        style_cell={
            'textAlign': 'center',
            'whiteSpace': 'normal',
            'height': 'auto',
            'minWidth': '120px', 'width': '120px', 'maxWidth': '200px',
            'font_size': '14px'
        },
        filter_action='native',
        page_action='none',
        sort_action='native',
        sort_mode='multi',
        editable=False
    )
])

# Callback per l'aggiornamento della tabella in base alla legislatura selezionata
@app.callback(
    Output('table', 'data'),
    [Input('legislatura-dropdown', 'value')]
)
def update_table(legislatura):
    filtered_df = df[df['legislatura'] == legislatura]
    return filtered_df.to_dict('records')

# Esegui l'applicazione Dash su Google Colab
if __name__ == '__main__':
    app.run_server(mode='inline')
