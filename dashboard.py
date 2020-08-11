# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 18:22:54 2020

@author: MasterDK-Laptop
"""
# import main libs
import os
import pandas as pd
import plotly.express as px

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output# Load Data

#fileurl = 'https://github.com/Printalect/Property-Listings-Dashboard/blob/master/property-listings-downsampled.csv'
fileurlraw = 'https://raw.githubusercontent.com/Printalect/Property-Listings-Dashboard/master/property-listings-downsampled.csv'
rawdata = pd.read_csv(fileurlraw)

# Dashboard one
plotdata = rawdata.groupby(['state', 'type'])['price'].mean().reset_index()
#plotdata.rename(columns={'id':'price'}, inplace=True)
typesconsidered = ['house', 'townhouse', 'apartment']

external_stylesheets1 = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#from jupyter_dash import JupyterDash
# app = JupyterDash(__name__, external_stylesheets=external_stylesheets1)
app =  dash.Dash(__name__, external_stylesheets=external_stylesheets1)
server = app.server

# Build App
#app = JupyterDash(__name__) #!!!!!
app.layout = html.Div([
    html.H2("Dashboard: Housing"),
    dcc.Graph(id='graph'),
    html.Label([
        "Type Selection",
        dcc.Dropdown(
            id='column-dropdown',
            clearable=False,
            value=typesconsidered[2],
            options=[{
                'label': c.title(),
                'value': c
            } for c in typesconsidered])
    ]),
])

# Define callback to update graph
@app.callback(Output('graph', 'figure'), [Input("column-dropdown", "value")])
def update_figure(column):
    return px.choropleth(plotdata[plotdata['type'] == column],
                            locations='state',
                            color='price',
                            locationmode='USA-states',
                            #hover_name='state'.title(),
                            #hover_data=['']
                            labels = {'price': 'Price'},
                            title='Mean Price: {}'.format(column.title())
                        )\
            .update_layout(
                geo_scope='usa',  # Plot only the USA instead of globe
            )

# app.run_server(debug=True, mode='inline', port=8058)


if __name__ == '__main__':
    app.run_server(debug=True)
