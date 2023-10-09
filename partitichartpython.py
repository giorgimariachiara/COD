import pandas as pd
import ipywidgets as widgets
import matplotlib.pyplot as plt

# Read your CSV data
df = pd.read_csv("partyallineamento.csv")

# Function to plot data based on alignment
def plot_data(alignment):
    # Filter data by alignment
    filtered_data = df[df['Allineamento Politico'] == alignment]
    
    # Count genders for each party
    gender_counts = filtered_data.groupby(['partito', 'gender']).size().unstack().fillna(0)
    
    # Plotting
    gender_counts.plot(kind='barh', stacked=True, figsize=(10,8))
    plt.title(f'Gender distribution for {alignment} parties')
    plt.xlabel('Count')
    plt.ylabel('Party')
    plt.show()

# Create an interactive widget
widgets.interact(plot_data, alignment=df['Allineamento Politico'].unique())
