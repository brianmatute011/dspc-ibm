#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
    'IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/'
    'historical_automobile_sales.csv'
)

# Convert Date to datetime and extract Year and Month
data['Date']  = pd.to_datetime(data['Date'])
data['Year']  = data['Date'].dt.year
data['Month'] = data['Date'].dt.month_name()

# Limit year range to 1980–2013
data = data[(data['Year'] >= 1980) & (data['Year'] <= 2013)]

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics',               'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics',     'value': 'Recession Period Statistics'}
]

# List of years 1980–2013
year_list = list(range(1980, 2014))

#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div   ([
    # TASK 2.1: Add title to the dashboard
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': '24px'
        }
    )
])



# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
