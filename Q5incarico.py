import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
from ipywidgets import interact

# Carica i dati dai file CSV in due DataFrame separati
df_men = pd.read_csv("contoincaricoMA.csv")
df_women = pd.read_csv("contoincaricoFE.csv")

# Estrai un elenco di tutte le legislature uniche
legislature = df_men['legislatura'].unique()

# Crea una funzione per generare la bar chart dinamica
@interact(legislatura=widgets.Dropdown(options=legislature, description='Legislatura:'))
def plot_bar_chart(legislatura):
    # Filtra i dati per la legislatura selezionata
    men_filtered = df_men[df_men['legislatura'] == legislatura]
    women_filtered = df_women[df_women['legislatura'] == legislatura]

    # Raggruppa i dati per incarico e calcola il conteggio di uomini e donne per ciascun incarico
    men_counts = men_filtered.groupby('incarico')['conto'].sum()
    women_counts = women_filtered.groupby('incarico')['conto'].sum()

    # Unisci i dati dei due generi in un unico DataFrame
    comparison_df = pd.DataFrame({'Uomini': men_counts, 'Donne': women_counts})

    # Crea la bar chart
    comparison_df.plot(kind='bar', stacked=True)
    plt.xlabel('Incarico')
    plt.ylabel('Numero di Deputati')
    plt.title(f'Confronto tra Deputati Uomini e Donne per Incarico - Legislatura {legislatura}')
    plt.legend(title='Genere', labels=['Uomini', 'Donne'])

    # Mostra solo 14 etichette per gli incarichi
    plt.xticks(range(len(comparison_df.index)), comparison_df.index, rotation=45, ha="right")

    plt.tight_layout()
    plt.show()
