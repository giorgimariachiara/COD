import pandas as pd
import plotly.graph_objects as go

# Read the CSV dataset using Pandas
data_male = pd.read_csv('graduatedMA.csv')

# Group data by legislature and count the number of graduated and non-graduated deputies for males
grouped_data_male = data_male.groupby('legislatura')['graduated'].value_counts().unstack().fillna(0)

# Create the bar chart for graduated and non-graduated male deputies using Plotly
fig_male = go.Figure()
fig_male.add_trace(go.Bar(
    x=grouped_data_male.index,
    y=grouped_data_male['yes'],
    name='Graduated',
    marker=dict(color='blue'),
    text=grouped_data_male['yes'],
    textposition='auto',
    hovertemplate='%{y} Graduated Male Deputies in Legislature %{x}<br>',
))
fig_male.add_trace(go.Bar(
    x=grouped_data_male.index,
    y=grouped_data_male['no'],
    name='Not Graduated',
    marker=dict(color='lightblue'),
    text=grouped_data_male['no'],
    textposition='auto',
    hovertemplate='%{y} Not Graduated Male Deputies in Legislature %{x}<br>',
))

# Customize the chart layout
fig_male.update_layout(
    title='Graduated and Non-Graduated Male Deputies in the Chamber of Deputies by Legislature',
    xaxis=dict(title='Legislature'),
    yaxis=dict(title='Number of Deputies'),
    barmode='stack',
)

# Display the chart
fig_male.show()
