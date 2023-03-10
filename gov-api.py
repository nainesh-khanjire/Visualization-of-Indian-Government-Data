import requests
import csv
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


# In this code, we first define the API endpoint and parameters for data.gov.in API, 
#and make a request to retrieve the data. We then write the data to a CSV file using Python's built-in csv module, and read the CSV file into a Pandas DataFrame.

# We create a Plotly Dash app by defining the layout using HTML and Dash components,
#and create a dropdown menu to select the x-axis field for the scatter plot. We define a callback function that updates the scatter plot based on the selected x-axis field.

# Finally, we run the app using app.run_server(debug=True). 
#Note that you will need to replace <YOUR_API_KEY> with your own API key for data.gov.in in order for the program to work.

# API endpoint for data.gov.in
url = 'https://api.data.gov.in/resource/f338e1f1-b527-454e-b0ee-089f3de3f0fa?api-key=579b464db66ec23bdd0000019c1bbfe2c0cc408879ac6ee4ae869d55&format=json'

# API parameters
params = {
    'api-key': '579b464db66ec23bdd0000019c1bbfe2c0cc408879ac6ee4ae869d55 ', 
    'format': 'json',
    'offset': 0,
    'limit': 100
}

# Make API request and extract data
response = requests.get(url, params=params)
data = response.json()['records']

# Write data to CSV file
with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(data[0].keys())
    for row in data:
        writer.writerow(row.values())

# Read data from CSV file
df = pd.read_csv('data.csv')


try:
# Create Plotly Dash app
    app = dash.Dash(__name__)

    app.layout = html.Div(children=[
        html.H1(children='My Data Visualization Dashboard'),

        html.Div(children='''
            Explore the data from data.gov.in
             '''),

        dcc.Dropdown(
            id='x-axis-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns],
            value=df.columns[0]
        ),

        dcc.Graph(
            id='my-graph'
        )
    ])

    @app.callback(
        Output('my-graph', 'figure'),
        Input('x-axis-dropdown', 'value')
    )
    def update_graph(x_axis):
        fig = px.scatter(df, x=x_axis, y='growth_rate___2022_23___q1')
        return fig


    if __name__ == '__main__':
        app.run_server(debug=True, use_reloader=False)
    
except Exception as e:
    print(str(e))
