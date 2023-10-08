import pandas as pd
import matplotlib.pyplot as plt

# Leggi il file CSV
df = pd.read_csv('quotepresidenti.csv')

# Filtra i dati per gli anni desiderati
anni = [2013, 2018, 2022]
df = df[df['anno'].isin(anni)]

# Raggruppa per anno e genere e conti il numero di presidenti
conteggio = df.groupby(['anno', 'genere']).size().unstack().fillna(0)

# Crea il grafico a barre
conteggio.plot(kind='bar', stacked=True, color=['green', 'purple'])

# Imposta il titolo e le etichette degli assi
plt.title('Presidenti dei gruppi parlamentari per anno e genere')
plt.xlabel('Anno')
plt.ylabel('Numero di presidenti')

# Mostra il grafico
plt.legend(title='Genere', labels=['Uomini', 'Donne'])
plt.show()
