import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Carica i dati dai file CSV
df_2013 = pd.read_csv("quote2013.csv")
df_2018 = pd.read_csv("quote2018.csv")
df_2022 = pd.read_csv("quote2022.csv")

# Unisce i dati in un unico DataFrame
df_all = pd.concat([df_2013, df_2018, df_2022], keys=["2013", "2018", "2022"], names=["Anno"])

# Crea una funzione per ottenere i gruppi parlamentari per un anno specifico
def get_gruppi_per_anno(anno):
    return sorted(df_all.xs(anno, level="Anno")["gruppoPar"].unique())

# Crea una funzione per generare il grafico
def generate_chart(selected_years, selected_group):
    filtered_df = df_all.loc[df_all.index.get_level_values("Anno").isin(selected_years)]

    if selected_group != "Tutti":
        filtered_df = filtered_df[filtered_df["gruppoPar"] == selected_group]

    fig = make_subplots(rows=1, cols=len(selected_years), subplot_titles=selected_years)
    

    colors = {"Uomini": "green", "Donne": "purple"}

    for i, year in enumerate(selected_years):
        filtered_year_df = filtered_df.xs(year, level="Anno")
        fig.add_trace(go.Bar(x=filtered_year_df["gruppoPar"], y=filtered_year_df["numeroUomini"], name="Uomini", legendgroup="Uomini", marker_color=colors["Uomini"]), row=1, col=i+1)
        fig.add_trace(go.Bar(x=filtered_year_df["gruppoPar"], y=filtered_year_df["numeroDonne"], name="Donne", legendgroup="Donne", marker_color=colors["Donne"]), row=1, col=i+1)
        

    fig.update_layout(barmode="group", title="Confronto tra uomini e donne nei gruppi parlamentari")
    fig.update_xaxes(title_text="Gruppo Parlamentare", categoryorder="category ascending")  # Imposta l'ordine delle categorie sull'asse x
    fig.update_yaxes(title_text="Numero di Individui")

    return fig

# Crea l'app Dash per l'interfaccia utente
import dash
from dash import dcc, html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Confronto tra uomini e donne nei gruppi parlamentari"),
    dcc.Dropdown(
        id="year-dropdown",
        options=[
            {"label": "2013", "value": "2013"},
            {"label": "2018", "value": "2018"},
            {"label": "2022", "value": "2022"}
        ],
        multi=True,
        value=["2013", "2022"]
    ),
    dcc.Dropdown(
        id="group-dropdown",
        value="Tutti"
    ),
    dcc.Graph(id="bar-chart")
])

@app.callback(
    dash.dependencies.Output("group-dropdown", "options"),
    dash.dependencies.Input("year-dropdown", "value")
)
def update_group_dropdown(selected_years):
    if not selected_years:
        return [{"label": "Tutti", "value": "Tutti"}]

    common_groups = set(get_gruppi_per_anno(selected_years[0]))
    for year in selected_years[1:]:
        common_groups &= set(get_gruppi_per_anno(year))

    group_options = [{"label": group, "value": group} for group in common_groups]
    group_options.insert(0, {"label": "Tutti", "value": "Tutti"})

    return group_options

@app.callback(
    dash.dependencies.Output("bar-chart", "figure"),
    dash.dependencies.Input("year-dropdown", "value"),
    dash.dependencies.Input("group-dropdown", "value")
)
def update_chart(selected_years, selected_group):
    return generate_chart(selected_years, selected_group)

if __name__ == "__main__":
    app.run_server(debug=True)
