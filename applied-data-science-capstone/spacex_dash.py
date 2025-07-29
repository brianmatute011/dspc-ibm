# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv('spacex_launch_geo.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Get unique launch sites for the dropdown
launch_sites = spacex_df['Launch Site'].unique()
site_options = [{'label': 'All Sites', 'value': 'ALL'}]
for site in launch_sites:
    site_options.append({'label': site, 'value': site})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a Launch Site Drop-down Input Component
                                dcc.Dropdown(id='site-dropdown',
                                             options=site_options,
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                             ),
                                html.Br(),

                                # Pie chart
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a Range Slider to Select Payload
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]
                                                ),
                                html.Br(),

                                # Scatter chart
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Calculate success counts for all sites
        fig = px.pie(spacex_df,
                     names='Launch Site',
                     values='class',
                     title='Total Success Launches by Site')
        return fig
    else:
        # Filter dataframe for selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Calculate success and failure counts
        success_count = filtered_df[filtered_df['class'] == 1].shape[0]
        failure_count = filtered_df[filtered_df['class'] == 0].shape[0]

        # Create pie chart
        fig = px.pie(names=['Success', 'Failure'],
                     values=[success_count, failure_count],
                     title=f'Success vs Failure for {entered_site}')
        return fig


# TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    # Filter dataframe based on payload range
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    filtered_df = spacex_df[mask]

    if entered_site == 'ALL':
        # Create scatter plot for all sites - CORREGIDO: 'Booster Version' en lugar de 'Booster Version Category'
        fig = px.scatter(filtered_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version',  # CORREGIDO AQUÍ
                         title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        # Filter dataframe for selected site
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        # Create scatter plot for selected site - CORREGIDO: 'Booster Version' en lugar de 'Booster Version Category'
        fig = px.scatter(site_filtered_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version',  # CORREGIDO AQUÍ
                         title=f'Correlation between Payload and Success for {entered_site}')
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)