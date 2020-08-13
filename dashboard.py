# Import main libs
import os
import pandas as pd
import plotly.express as px
# Dash libs
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output  # Load Data

sourcelink = 'https://www.kaggle.com/austinreese/usa-housing-listings'
fileurlraw ='https://raw.githubusercontent.com/Printalect/Property-Listings-Dashboard/master/assets/property-listings-100000-d2.csv'
rawdata    = pd.read_csv(fileurlraw)
#plotdata = rawdata.copy()

type_options = ['house', 'townhouse', 'apartment']
category_options = [
    'baths', 'beds', 'cats_allowed', 'dogs_allowed',
    'electric_vehicle_charge', 'laundry_options', 'parking_options',
    'smoking_allowed', 'wheelchair_access'
]

# still need to implement this if there are not eough values!
rawdata = rawdata[rawdata['type'].isin(type_options)]
rawdata = rawdata.groupby('state').filter(
    lambda x: len(x) >= 100)  # only listings of 100 or more
rawdata.reset_index(inplace=True)

# create a dict for state regions
states_regions = rawdata[['state', 'region']]
states_regions = states_regions.groupby('state')#.agg(counts=('region', 'count'))
states_regions = states_regions['region'].unique().apply(list).to_dict()

#app = JupyterDash(__name__, external_stylesheets=[dbc.themes.LUX])
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

dropdown_style_options = {
    'width': '100%',
    'display': 'flex',
    'align-items': 'center',
    'justify-content': 'center'
}

maintitle = html.Div(
    [dbc.Row([(html.H1("Property Rent Listings Dashboard"))], justify="center")])
#dbc.Row([(html.H2("National Data"))],justify="center"),
#dbc.Row(dbc.Col(html.Div()))
#--------------
#-NATIIONAL
nationallevel = html.Div([
    #dbc.Row([(html.H2("National Data"))],justify="center"),
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='national_graph1'))),
        dbc.Col(html.Div(dcc.Graph(id='national_graph2')))
    ])
])

nationalselector = html.Div([
    dbc.Row([(html.H2("National Data"))], justify="center"),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Label([
                    "Type Selection (National):",
                    dcc.Dropdown(id='national_dropdown_type',
                                 clearable=False,
                                 multi=True,
                                 value=type_options,
                                 options=[{
                                     'label': type_options[0].title(),
                                     'value': type_options[0]
                                 }, {
                                     'label': type_options[1].title(),
                                     'value': type_options[1]
                                 }, {
                                     'label': type_options[2].title(),
                                     'value': type_options[2]
                                 }])
                ])
            ],
                     style=dropdown_style_options))
    ])
])
#-NATIIONAL
#--------------

#--------------
#-STATE-LEVEL
statelevel = html.Div([
    #dbc.Row([(html.H2("State Data"))],justify="center"),
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='state_graph1'))),
        dbc.Col(html.Div(dcc.Graph(id='state_graph2')))
    ])
])

statelevelselector = html.Div([
    dbc.Row([(html.H2("State Data"))], justify="center"),
    dbc.Row([
        dbc.Col(
            html.Div(
                [
                    html.Label([
                        "Type Selection (State):",
                        dcc.Dropdown(
                            id='states_dropdown_type',
                            #clearable=False,
                            multi=True,
                            value=type_options,
                            #justify='center',
                            options=[{
                                'label': type_options[0].title(),
                                'value': type_options[0]
                            }, {
                                'label': type_options[1].title(),
                                'value': type_options[1]
                            }, {
                                'label': type_options[2].title(),
                                'value': type_options[2]
                            }])
                    ]),
                    html.Label([
                        "State Selection: ",
                        dcc.Dropdown(id='state_level_states_dropdown',
                                     clearable=False,
                                     value='CA',
                                     options=[{
                                         'label': k,
                                         'value': k
                                     } for k in states_regions.keys()])
                    ])
                ],
                style=dropdown_style_options))
    ])
])

#-STATE-LEVEL
#--------------

#--------------
#-REGION-LEVEL
regionlevel = html.Div([
    #dbc.Row([(html.H2("Region (City & County)"))],justify="center"),
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='region_graph1'))),
        dbc.Col(html.Div(dcc.Graph(id='region_graph2')))
    ])
])

regionlevelselector = html.Div([
    dbc.Row([(html.H2("Region (City & County)"))], justify="center"),
    dbc.Row([
        dbc.Col(
            html.Div(
                [
                    html.Label([
                        "Type Selection (Region):",
                        dcc.Dropdown(
                            id='region_dropdown_type',
                            #clearable=False,
                            multi=True,
                            value=type_options,
                            #justify='center',
                            options=[{
                                'label': type_options[0].title(),
                                'value': type_options[0]
                            }, {
                                'label': type_options[1].title(),
                                'value': type_options[1]
                            }, {
                                'label': type_options[2].title(),
                                'value': type_options[2]
                            }])
                    ]),
                    html.Label([
                        "State Selection:",
                        dcc.Dropdown(id='region_level_states_dropdown',
                                     clearable=False,
                                     value='CA',
                                     options=[{
                                         'label': k,
                                         'value': k
                                     } for k in states_regions.keys()])
                    ]),
                    html.Label(
                        [
                            "Region Selection: ",
                            dcc.Dropdown(id='regions_dropdown',
                                         #multi=True
                                         )
                        ],
                        style={'width': '300px'})
                ],
                style=dropdown_style_options)),
    ]),
])

#-REGION-LEVEL
#--------------


#--------------
#-ADDITIONAL
sourcelinks = html.Div([
    #dbc.Row([(html.H2("Region (City & County)"))],justify="center"),
    dbc.Row([
        dbc.Col(html.Div(html.A('Data Source (click)', href=sourcelink, target='_blank')), style=dropdown_style_options),
    ])
])


blankrow = html.Div([dbc.Row([html.Br()])], style={'marginBottom': '1.5em'})

#-ADDITIONAL
#--------------



#  - - - -
app.layout = html.Div([
    maintitle, blankrow, nationalselector, nationallevel, blankrow,
    statelevelselector, statelevel, blankrow, regionlevelselector, regionlevel,
    blankrow, sourcelinks
])


#  - - - -
#--------------v
#-NATIIONAL
# Define callback to update graph
@app.callback(Output('national_graph1', 'figure'),
              [Input("national_dropdown_type", "value")])
def update_figure(plot_type):
    plotdata = rawdata[(rawdata['type'].isin(plot_type))]
    plotdata = plotdata.groupby('state').agg(avg_price=('price', 'mean'))
    plotdata = plotdata.reset_index()
    return px.choropleth(
                        plotdata,
                        locations='state',
                        color='avg_price',
                        locationmode='USA-states',
                        title=('Mean Price by State'),
                        labels={'avg_price':'Avg Price',
                                'price': 'Price',
                                'state':'State',
                               'count':'Count'},
                        color_continuous_scale=px.colors.sequential.Blues
                    )\
        .update_layout(
            geo_scope='usa' # Plot only the USA instead of globe
        )


# Define callback to update graph
@app.callback(Output('national_graph2', 'figure'),
              [Input("national_dropdown_type", "value")])
def update_figure(plot_type):
    plotdata = rawdata[(rawdata['type'].isin(plot_type))]
    plotdata = plotdata.groupby('state').agg(count=('state', 'count'))
    plotdata = plotdata.reset_index().sort_values('count', ascending=False)
    plotdata = plotdata.dropna(subset=['count'], axis=0)
    return px.bar(
        plotdata[0:20],
        x='state',
        y='count',
        color='count',
        opacity=0.8,
        title=('Total Properties Per State'),
        labels={
            'avg_price': 'Avg Price',
            'price': 'Price',
            'state': 'State',
            'count': 'Count',
            'region': 'Region'
        },
        color_continuous_scale=px.colors.sequential.Blues,
    ).update_xaxes(categoryorder='total descending')


#-NATIIONAL
#--------------^


#--------------v
#-STATE-LEVEL
# Define callback to update graph
@app.callback(Output('state_graph1', 'figure'), [
    Input("states_dropdown_type", "value"),
    Input("state_level_states_dropdown", "value")
])
def update_figure(plot_type, plot_state):
    plotdata = rawdata
    return px.scatter_mapbox(
        plotdata[(plotdata['type'].isin(plot_type))
                 & (plotdata['state'] == plot_state)],
        lat="lat",
        lon="long",
        color="price",
        size="price",
        mapbox_style="carto-positron",
        text='state',
        hover_name='type',
        hover_data=['type', 'price', 'sqfeet', 'baths', 'beds'],
        #title=('Listing Data by Price & Type in {}'.format(str(plotstate))),
        color_continuous_scale=px.colors.sequential.Blues,
        size_max=15,
        zoom=4,
        title=('Detailed Information Per Listing in {}'.format(
            str(plot_state))),
        labels={
            'avg_price': 'Avg Price',
            'price': 'Price',
            'state': 'State',
            'count': 'Count',
            'type': 'Type',
            'sqfeet': 'SQ FT',
            'baths': 'Baths',
            'beds': 'Beds'
        },
        height=500)


@app.callback(Output('state_graph2', 'figure'), [
    Input("states_dropdown_type", "value"),
    Input("state_level_states_dropdown", "value")
])
def update_figure(plot_type, plot_state):
    plotdata = rawdata[(rawdata['state'] == plot_state)
                       & (rawdata['type'].isin(plot_type))]
    plotdata = plotdata.groupby('region').agg(count=('region', 'count'))
    plotdata = plotdata.reset_index().sort_values('count', ascending=False)
    plotdata = plotdata.dropna(subset=['count'], axis=0)
    return px.bar(
        plotdata[0:20],
        x='region',
        y='count',
        color='count',
        opacity=0.8,
        color_continuous_scale=px.colors.sequential.Blues,
        title=('Total Properties Per Region in {}'.format(str(plot_state))),
        labels={
            'avg_price': 'Avg Price',
            'price': 'Price',
            'state': 'State',
            'region': 'Region',
            'count': 'Count',
            'type': 'Type',
            'sqfeet': 'SQ FT',
            'baths': 'Baths',
            'beds': 'Beds',
        },
    ).update_xaxes(categoryorder='total descending')

#-STATE-LEVEL
#--------------^


#--------------
#-REGION-LEVEL
@app.callback(
    dash.dependencies.Output('regions_dropdown', 'options'),
    [dash.dependencies.Input('region_level_states_dropdown', 'value')])
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in states_regions[selected_country]]

@app.callback(dash.dependencies.Output('regions_dropdown', 'value'),
              [dash.dependencies.Input('regions_dropdown', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']


# Define callback to update graph
@app.callback(Output('region_graph1', 'figure'), [
    Input("region_dropdown_type", "value"),
    Input("region_level_states_dropdown", "value")
])
def update_figure(plot_type, plot_state):
    plotdata = rawdata[(rawdata['state'] == plot_state)
                       & (rawdata['type'].isin(plot_type))]
    plotdata = plotdata.groupby('region').agg(avg_price=('price', 'mean'))
    plotdata = plotdata.reset_index().sort_values('avg_price', ascending=False)
    plotdata = plotdata.dropna(subset=['avg_price'], axis=0)
    return px.bar(
        plotdata[0:20],
        x='region',
        y='avg_price',
        color='avg_price',
        opacity=0.8,
        title=('Average Price, Regions in {}'.format(str(plot_state))),
        labels={
            'avg_price': 'Avg Price',
            'price': 'Price',
            'state': 'State',
            'count': 'Count',
            'region': 'Region'
        },
        color_continuous_scale=px.colors.sequential.Blues,
    )


# Define callback to update graph
@app.callback(Output('region_graph2', 'figure'), [
    Input("region_dropdown_type", "value"),
    Input("region_level_states_dropdown", "value"),
    Input("regions_dropdown", "value")
])
def update_figure(plot_type, plot_state, plot_region):
    plotdata = rawdata.copy()
    return px.histogram(
        plotdata[(plotdata['type'].isin(plot_type))
                 & (plotdata['state'] == plot_state)
                 & (plotdata['region'].isin([plot_region]))],
        x='price',
        color='region',
        #nbins=50,
        #histnorm='density',
        marginal='violin',
        opacity=0.8,
        title=('Price Distribution: {}'.format(str(plot_region))),
        labels={
            'avg_price': 'Avg Price',
            'price': 'Price',
            'state': 'State',
            'count': 'Count',
            'region': 'Region'
        },
        color_discrete_sequence=px.colors.sequential.Blues_r)

#-REGION-LEVEL
#--------------

#app.run_server(debug=True, mode='external', port=8106)
if __name__ == '__main__':
    app.run_server(debug=False, port=8051)
