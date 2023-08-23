import pandas as pd
import plotly.graph_objects as go

# Carica i dati degli incarichi per uomini e donne dai file CSV
df_uomini = pd.read_csv('incaricoMALE.csv')
df_donne = pd.read_csv('incaricoFEMALE.csv')

# Lista delle legislature disponibili
legislature_list = df_uomini['legislatura'].unique()
legislature_order = ['costituente', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']

# Funzione per impostare la scala dell'asse radiale da 0 a 200 con step di 10
def set_radial_axis_scale():
    return [0, 200]
# Funzione per impostare la scala dell'asse radiale con dtick condizionale
def set_radial_axis_scale():
    return [0, 50, 200], 10 if df_uomini['incarico'].max() <= 50 else 50

# Crea la radar chart iniziale
def update_radar_chart(selected_legislatura):
    max_value = max(df_uomini['incarico'].value_counts().max(), df_donne['incarico'].value_counts().max())

    fig = go.Figure()

    # Opzioni per il grafico a radar
    options = {
        'theta': df_uomini['incarico'].unique(),
        'name': 'Uomini',
        'fill': 'toself',
        'fillcolor': 'rgba(0, 139, 139, 0.2)',
        'line': {'color': 'rgba(0, 139, 139, 1)'},
    }

    # Aggiungi il primo trace per gli uomini
    fig.add_trace(go.Scatterpolar(**options))

    # Opzioni per le donne
    options['name'] = 'Donne'
    options['fillcolor'] = 'rgba(220, 20, 60, 0.2)'
    options['line'] = {'color': 'rgba(220, 20, 60, 1)'}

    # Aggiungi il secondo trace per le donne
    fig.add_trace(go.Scatterpolar(**options))

    # Aggiungi le informazioni per il layout del grafico
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=set_radial_axis_scale(), dtick=10, tickfont=dict(size=12)),
            radialaxis=dict(visible=True, range=set_radial_axis_scale()[0], dtick=set_radial_axis_scale()[1], tickfont=dict(size=12)),
        ),
        showlegend=True,
        title='Incarichi per Legislatura',
        updatemenus=[
            {
                'buttons': [
                    {
                        'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}],
                        'label': 'Play',
                        'method': 'animate',
                    },
                    {
                        'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                        'label': 'Pause',
                        'method': 'animate',
                    },
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 87},
                'showactive': False,
                'type': 'buttons',
                'x': 0.1,
                'xanchor': 'right',
                'y': 0,
                'yanchor': 'top',
            }
        ],
        sliders=[{
            'active': 0,
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 20},
                'prefix': 'Legislatura: ',
                'visible': True,
                'xanchor': 'right'
            },
            'transition': {'duration': 300, 'easing': 'cubic-in-out'},
            'pad': {'b': 10, 't': 50},
            'len': 0.9,
            'x': 0.1,
            'y': 0,
            'steps': [
                {
                    'args': [[str(legislatura)], {'frame': {'duration': 300, 'redraw': True}, 'mode': 'immediate'}],
                    'label': str(legislatura),
                    'method': 'animate',
                }
                for legislatura in legislature_order
            ],
        }],
    )

    # Crea le animazioni per le diverse legislature
    frames = [
        go.Frame(
            data=[
                go.Scatterpolar(
                    r=df_donne[df_donne['legislatura'] == legislatura]['incarico'].value_counts().reindex(df_uomini['incarico'].unique(), fill_value=0).values * 200 / max_value,
                    theta=df_uomini['incarico'].unique(),
                    fill='toself',
                    fillcolor='rgba(220, 20, 60, 0.2)',
                    line={'color': 'rgba(220, 20, 60, 1)'},
                    name='Donne',
                    hoverinfo='name+r',
                ),
                go.Scatterpolar(
                    r=df_uomini[df_uomini['legislatura'] == legislatura]['incarico'].value_counts().reindex(df_uomini['incarico'].unique(), fill_value=0).values * 200 / max_value,
                    theta=df_uomini['incarico'].unique(),
                    fill='toself',
                    fillcolor='rgba(0, 139, 139, 0.2)',
                    line={'color': 'rgba(0, 139, 139, 1)'},
                    name='Uomini',
                    hoverinfo='name+r',
                ),
            ],
            name=str(legislatura),
        )
        for legislatura in legislature_order
    ]

    fig.update(frames=frames)

    # Mostra il grafico
    fig.show()

# Crea la radar chart iniziale
update_radar_chart('costituente')
