import pandas as pd
import matplotlib.pyplot as plt

# Carica i dati dal file CSV
df = pd.read_csv('totaledeputati.csv')

# Conta il numero di deputati per genere
gender_counts = df['gender'].value_counts()

# Crea la bar chart
plt.bar(gender_counts.index, gender_counts.values)

# Aggiungi etichette
plt.xlabel('Genere')
plt.ylabel('Numero deputati')
plt.title('Numero deputati per genere')

# Mostra la bar chart
plt.show()
