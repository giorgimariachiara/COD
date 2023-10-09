import pandas as pd

# Lista dei nomi dei file CSV di input
input_files = ['quote2018.csv', 'quote2022.csv', 'quote2013.csv']

for input_file in input_files:
    # Leggi il file CSV di input
    df = pd.read_csv(input_file)

    # Calcola le percentuali di uomini e donne e arrotonda ai numeri interi
    df['PercentualeDonne'] = ((df['numeroDonne'] / (df['numeroDonne'] + df['numeroUomini'])) * 100).round().astype(int)
    df['PercentualeUomini'] = ((df['numeroUomini'] / (df['numeroDonne'] + df['numeroUomini'])) * 100).round().astype(int)

    # Genera il nome del nuovo file CSV di output
    output_file = input_file.replace('.csv', '_percentuali.csv')

    # Salva il DataFrame modificato in un nuovo file CSV
    df.to_csv(output_file, index=False)

print("Percentuali arrotondate e file CSV generati con successo.")
