#!/usr/bin/env python
# coding: utf-8
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"></ul></div>

# import main libs
import os 
import pandas as pd
import numpy as np
from pandas import DataFrame as DFM
import warnings
warnings.filterwarnings('ignore')

import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly as py
init_notebook_mode(connected=True)

from jupyter_dash import JupyterDash
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
app = JupyterDash(__name__, external_stylesheets=external_stylesheets1)

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
    app.run_server()


if __name__ == '__main__':
    app.run_server()
