import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html

# Carica i dati dai file CSV
df_2013 = pd.read_csv("quote2013.csv")
df_2018 = pd.read_csv("quote2018.csv")
df_2022 = pd.read_csv("quote2022.csv")

# Unisce i dati in un unico DataFrame
df_all = pd.concat([df_2013, df_2018, df_2022], keys=["2013", "2018", "2022"], names=["Anno"])

# Crea l'app Dash per l'interfaccia utente
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
    dcc.Graph(id="stacked-bar-chart")
])

@app.callback(
    dash.dependencies.Output("group-dropdown", "options"),
    dash.dependencies.Input("year-dropdown", "value")
)
def update_group_dropdown(selected_years):
    if not selected_years:
        return [{"label": "Tutti", "value": "Tutti"}]

    common_groups = set(df_all[df_all.index.get_level_values("Anno").isin(selected_years)]["gruppoPar"].unique())
    group_options = [{"label": group, "value": group} for group in common_groups]
    group_options.insert(0, {"label": "Tutti", "value": "Tutti"})

    return group_options

@app.callback(
    dash.dependencies.Output("stacked-bar-chart", "figure"),
    dash.dependencies.Input("year-dropdown", "value"),
    dash.dependencies.Input("group-dropdown", "value")
)
def update_stacked_bar_chart(selected_years, selected_group):
    filtered_df = df_all[df_all.index.get_level_values("Anno").isin(selected_years)]

    if selected_group != "Tutti":
        filtered_df = filtered_df[filtered_df["gruppoPar"] == selected_group]

    # Raggruppa per anno e gruppo parlamentare e calcola le somme
    grouped_df = filtered_df.groupby(["Anno", "gruppoPar"]).sum().reset_index()

    # Calcola le percentuali di uomini e donne
    grouped_df["percentualeUomini"] = (grouped_df["numeroUomini"] / (grouped_df["numeroUomini"] + grouped_df["numeroDonne"])) * 100
    grouped_df["percentualeDonne"] = (grouped_df["numeroDonne"] / (grouped_df["numeroUomini"] + grouped_df["numeroDonne"])) * 100

    fig = go.Figure()

    for year in selected_years:
        filtered_year_df = grouped_df[grouped_df["Anno"] == year]
        fig.add_trace(go.Bar(x=filtered_year_df["gruppoPar"], y=filtered_year_df["percentualeUomini"], name=f"{year} - Uomini", marker_color="green"))
        fig.add_trace(go.Bar(x=filtered_year_df["gruppoPar"], y=filtered_year_df["percentualeDonne"], name=f"{year} - Donne", marker_color="purple"))

    fig.update_layout(barmode="stack", title="Percentuale di uomini e donne nei gruppi parlamentari")
    fig.update_xaxes(title_text="Gruppo Parlamentare", categoryorder="category ascending")  
    fig.update_yaxes(title_text="Percentuale")

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
