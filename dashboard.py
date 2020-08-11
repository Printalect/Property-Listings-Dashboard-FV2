# import main libs
import os
import pandas as pd
import plotly.express as px

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output# Load Data

fileurlraw = 'https://raw.githubusercontent.com/Printalect/Property-Listings-Dashboard/master/property-listings-downsampled.csv'
rawdata = pd.read_csv(fileurlraw)

# Dashboard Two
typesconsidered = ['house', 'townhouse', 'apartment']
plotdata = rawdata[rawdata['type'].isin(typesconsidered)]
plotdata = plotdata.groupby('state').filter(
    lambda x: len(x) >= 100)  # only listings of 100 or more
#plotdata.set_index('id',inplace=True)
statesconsidered = sorted(list(set(plotdata['state'])))

external_stylesheets1 = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app =  dash.Dash(__name__, external_stylesheets=external_stylesheets1)
server = app.server

# Build App
app.layout = html.Div([
    html.H2("Dashboard: Housing"),
    dcc.Graph(id='graph'),
    html.Label([
        "Type Selection",
        dcc.Dropdown(id='column-dropdown-type',
                     clearable=False,
                     value=typesconsidered[2],
                     options=[{
                         'label': c.title(),
                         'value': c
                     } for c in typesconsidered]),
    ]),
    html.Label([
        "State Selection",
        dcc.Dropdown(id='column-dropdown-state',
                     clearable=False,
                     value=statesconsidered[0],
                     options=[{
                         'label': c,
                         'value': c
                     } for c in statesconsidered])
    ]),
])

# Define callback to update graph
@app.callback(Output('graph', 'figure'), [
    Input("column-dropdown-type", "value"),
    Input("column-dropdown-state", "value")
])

def update_figure(plottype, plotstate):
    fig = px.scatter_mapbox(
        plotdata[(plotdata['type'] == plottype)
                 & (plotdata['state'] == plotstate)],
        lat="lat",
        lon="long",
        color="price",
        size="price",
        mapbox_style="carto-positron",
        hover_name='type',
        hover_data=['type', 'price', 'sqfeet', 'baths', 'beds'],
        #color_discrete_sequence=px.colors.qualitative.Set3,
        #title = 'Listing Selection by State: {} & Type: {}'.format(plotstate, plotype),
        size_max=15,
        zoom=4.5)
    return fig

if __name__ == '__main__':
    app.run_server()
