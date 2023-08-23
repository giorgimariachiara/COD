
import pandas as pd
import plotly.graph_objects as go
from natsort import index_natsorted

# Read the CSV dataset with modified legislature names using Pandas
data = pd.read_csv('graduatedMALE.csv')

# Define a function to convert the legislature name to a sortable format
def custom_sort_key(legislature):
    if 'Costituente' in legislature:
        return (0, 0)  # Sort the "Legislatura Costituente" first
    else:
        num_part = ''.join(filter(str.isdigit, legislature))
        num_part = int(num_part) if num_part else 0
        return (1, num_part)  # Sort other legislatures with numerical values

# Create an index using natsorted to maintain the natural sorting order
index_order = index_natsorted(data['legislatura'], key=custom_sort_key)

# Apply the custom sorting order to the DataFrame
data = data.loc[index_order]

# Define the custom order for legislatures
custom_legislature_order = [
    'Legislatura Costituente',
    'Legislatura 1',
    'Legislatura 2',
    'Legislatura 3',
    'Legislatura 4',
    'Legislatura 5',
    'Legislatura 6',
    'Legislatura 7',
    'Legislatura 8',
    'Legislatura 9',
    'Legislatura 10',
    'Legislatura 11',
    'Legislatura 12',
    'Legislatura 13',
    'Legislatura 14',
    'Legislatura 15',
    'Legislatura 16',
    'Legislatura 17',
    'Legislatura 18',
    'Legislatura 19'
]

# Reorder the 'legislatura' column based on the custom order
data['legislatura'] = pd.Categorical(data['legislatura'], categories=custom_legislature_order, ordered=True)
data = data.sort_values('legislatura')

# Calculate the total number of deputies by legislature
legislature_counts = data['legislatura'].value_counts()

# Calculate the number of graduated and non-graduated deputies by legislature
graduated_counts = data[data['graduated'] == 'yes']['legislatura'].value_counts()
non_graduated_counts = legislature_counts - graduated_counts

# Calculate the percentage of graduated deputies by legislature
import pandas as pd
import plotly.graph_objects as go

# Read the CSV dataset using Pandas
data = pd.read_csv('graduatedMALE.csv')

# Define the correct order for legislatures
legislature_order = ['costituente', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']

# Convert 'legislatura' column to categorical with the correct order
data['legislatura'] = pd.Categorical(data['legislatura'], categories=legislature_order, ordered=True)

# Calculate the total number of deputies by legislature in the correct order
legislature_counts = data['legislatura'].value_counts().sort_index()

# Calculate the number of graduated and non-graduated deputies by legislature in the correct order
graduated_counts = data[data['graduated'] == 'yes']['legislatura'].value_counts().sort_index()
non_graduated_counts = legislature_counts - graduated_counts

# Calculate the percentage of graduated deputies by legislature in the correct order
percentage_graduated = (graduated_counts / legislature_counts) * 100

# Create the Mekko bar chart using Plotly
fig = go.Figure(data=[
    go.Bar(
        x=graduated_counts.index,
        y=graduated_counts.values,
        name='Graduated',
        marker=dict(color='green'),
        text=percentage_graduated.values.round(2),
        textposition='auto',
        texttemplate='%{text:.2f}%',
        hovertemplate='%{y} Graduated<br>%{text} of Total<br>',
    ),
    go.Bar(
        x=non_graduated_counts.index,
        y=non_graduated_counts.values,
        name='Non-Graduated',
        marker=dict(color='purple'),
        hovertemplate='%{y} Non-Graduated<br>',
    )
])

# Customize the chart layout
fig.update_layout(
    title='Proportion of Graduated and Non-Graduated Deputies by Legislature',
    xaxis=dict(title='Legislature'),
    yaxis=dict(title='Number of Deputies'),
    barmode='stack',
    legend=dict(title='Status'),
)

# Display the chart
fig.show()
