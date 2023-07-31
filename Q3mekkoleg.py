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
