import pandas as pd
import matplotlib.pyplot as plt

# Leggi il file CSV
df = pd.read_csv('quotepresidenti.csv')

# Filtra i dati solo per gli anni desiderati (2013, 2018, 2022)
anni_desiderati = [2013, 2018, 2022]
df = df[df['start'].isin(anni_desiderati)]

# Conta il numero di presidenti per genere
conteggio_uomini = df[df['gender'] == 'male'].groupby('start').size()
conteggio_donne = df[df['gender'] == 'female'].groupby('start').size()

# Crea il grafico a barre solo per gli anni desiderati
plt.bar(anni_desiderati, conteggio_uomini, color='green', label='Uomini')
plt.bar(anni_desiderati, conteggio_donne, color='purple', label='Donne', bottom=conteggio_uomini)

# Imposta il titolo e le etichette degli assi
plt.title('Presidenti dei gruppi parlamentari per anno e genere')
plt.xlabel('Anno')
plt.ylabel('Numero di presidenti')

# Mostra il grafico
plt.legend(title='Genere')
plt.show()
