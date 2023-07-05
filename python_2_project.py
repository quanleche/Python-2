import os
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import numpy as np
import dash_mantine_components as dmc
import geopandas as gpd

gdp = pd.read_csv("GDP Dataset.csv")
countryfile = "ne_110m_admin_0_countries.shp"
gdf = gpd.read_file(countryfile)[['ADMIN', 'ADM0_A3']]
gdf.columns = ['Country', 'Country Code']

gdf.replace(to_replace= "United States of America", value = "United States", inplace=True)
gdf.replace(to_replace= "North Korea", value = "Korea, North", inplace=True)
gdf.replace(to_replace= "South Korea", value = "Korea, South", inplace=True)
gdf.replace(to_replace= "Ivory Coast", value = "Cote d'Ivoire", inplace=True)
gdf.replace(to_replace= "Democratic Republic of the Congo", value = "DR Congo", inplace=True)
gdf.replace(to_replace= "United Republic of Tanzania", value = "Tanzania", inplace=True)

GDP = gdp[["Country", "Population", "GDP","Continent"]]
merged = gdf.merge(GDP, left_on = "Country", right_on = "Country", how = "left")

merged = merged.fillna(0)
merged['GDP'] = merged['GDP'].astype(float)
merged = merged.drop(merged[merged['GDP'] <= 0].index)
merged_sorted = merged.sort_values('GDP', ascending=False)

TITLE = html.Div(
    style={
        'backgroundColor':'white'
    },
    children=[
                dmc.Header(height = 30, fixed = True, pl=0, pr=0, pt=0, style={'background-color':'orange', 'color':'whitesmoke'},
                   children=[
                       dmc.Text("VIETNAMESE - GERMAN UNIVERSITY", color='dark', size='xl', 
                                style={'font-family':'Georgia', 
                                       'margin-left':10})
                   ]),
    html.Div(
        style={
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'center'
        },
        children=[
            html.A(
   html.Img(
        src='https://images.plot.ly/logo/new-branding/plotly-logomark.png',
        height='25px',
        width='25px'
    ),
    title='Data Link',
    href='https://drive.google.com/file/d/14m9IVuuJmh3TsV4ANvyNLcDwHPqc5gIo/view?usp=drive_link',
    style={
        "boxShadow": f"0px 0px 0px 2px {'grey'}",
        "borderRadius": "10px",
        "padding": "5px",
        "color": "black",
        "textShadow": f"0px 0px 10px {'blue'}",
        "background-color": "white"
    }
),
            html.H1(
    children="GLOBAL ECONOMY",
    style={
        "fontSize": 40,
        "textAlign": "center",
        "color": "navy",
        "background": "white",
        "padding": "10px",
        "border": "2px solid black",
        "borderRadius": "10px",
        "boxShadow": f"0px 0px 0px 1px {'black'}",
        "font-family":"Georgia"
    }
)
        ]
    )
    ]
)  
CONDITION = html.Div(
        [
        html.P('(Less than 15 countries in Oceania have data)',
               style={
                   "fontsize": 5,
                   "color": 'gray',
                   "font-family": 'Georgia',
                   "font-weight": 'lighter'
               }),
        dcc.Dropdown(
            gdp['Continent'].unique(), id="continent-drop", clearable=False, 
            style={
                "marginBottom": 50, 
                "font-size": 12,
                "background": 'bisque'
                }
                ),
        dcc.Slider(
            id="selection-slider",
            min=0, max=30,
            step=1,
            marks={
                0:'0', 
                5:'5', 
                10:'10', 
                15:'15', 
                20:'20', 
                25:'25', 
                30:'30', }
        ),
        html.P('(Selected data will be applied for all charts. Legends can also be used)',
               style={
                   "fontsize": 5,
                   "color": 'gray',
                   "font-family": 'Georgia',
                   "font-weight": 'lighter'
               })
        ]
)
CONDITION2 = html.Div(
        dcc.RangeSlider(
            id="range-slider",
            min=merged['GDP'].min(), 
            max=20000000,
            marks={
                0:'0',
                2000000:'2M', 
                4000000:'4M',
                6000000:'6M', 
                8000000:'8M', 
                10000000:'10M',
                12000000:'12M',
                14000000:'14M',
                16000000:'16M',
                18000000:'18M',
                20000000:'20M'
                }),
            style = {
            "margin-top": '30px',
            "margin-bottom": '15px'
            }
)
GDP_HAPPINESS = [
    dbc.CardHeader(html.H5("GDP and Happiness index",
                           style={
                               "fontSize": 20,
                               "textAlign": "center",
                               "color": "black",
                               "background": "white",
                               "padding": "10px",
                               "border": "2px dashed black",
                               "borderRadius": "10px",
                               "boxShadow": f"0px 0px 0px 1px {'black'}",
                               "font-family":"Georgia"
                           })),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Tabs(
                                id="tabs1",
                                children=[
                                    dcc.Tab(
                                        label="Treemap", 
                                        style={
                                            "background": "bisque",
                                            'color': 'black',
                                            'border': 'grey',
                                            'font-size': '25px',
                                            'align-items': 'center',
                                            'justify-content': 'center',
                                            'border-radius': '10px',
                                            'padding':'6px'
                                        },
                                        selected_style={
                                            "background": "black",
                                            'color': 'white',
                                            'border': 'grey',
                                            'font-size': '25px',
                                            'align-items': 'center',
                                            'justify-content': 'center',
                                            'border-radius': '10px',
                                            'padding':'6px'
                                        },
                                        children=[
                                            dcc.Loading(
                                                id="loading-treemap",
                                                children=[
                                                    html.Div(dcc.Graph(id="continent3-treemap",
                                                                       style = {"border": '1px solid white'}), 
                                                             style={"float":'left'})
                                                    ],
                                                type="default"
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label="Scatterplot",
                                        style = {
                                            "background": "bisque",
                                            'color': 'black',
                                            'border': 'grey',
                                            'font-size': '25px',
                                            'align-items': 'center',
                                            'justify-content': 'center',
                                            'border-radius': '10px',
                                            'padding':'6px'
                                        },
                                        selected_style = {
                                            "background": "black",
                                            'color': 'white',
                                            'border': 'grey',
                                            'font-size': '25px',
                                            'align-items': 'center',
                                            'justify-content': 'center',
                                            'border-radius': '10px',
                                            'padding':'6px'
                                        },
                                        children=[
                                            dcc.Loading(
                                                id="loading-scatter-plot",
                                                children=[
                                                    html.Div(dcc.Graph(id="continent1-scatter",
                                                                       style = {"border": '1px solid white'}), 
                                                             style={"float":'left'})
                                                ],
                                                type="default"
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                    ),
                ]
            )
        ]
    ),
]
BAR_PLOT = dcc.Loading(
    id="loading-bar-plot", children=[dcc.Graph(id="continent2-barchart",
                                               style = {"border": '1px solid white'})], type="default"
)
BAR = [
    dbc.CardHeader(html.H5("Top countries of each continent",
                           style={
                               "fontSize": 20,
                               "textAlign": "center",
                               "color": "black",
                               "background": "white",
                               "padding": "10px",
                               "border": "2px dashed black",
                               "borderRadius": "10px",
                               "boxShadow": f"0px 0px 0px 1px {'black'}",
                               "font-family":"Georgia"
                           })),
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([
                    BAR_PLOT
                ])
            ])
        ]
    )
]
BOXPLOT = [
    dbc.CardHeader(html.H5("Distribution of GDP",
                           style={
                               "fontSize": 20,
                               "textAlign": "center",
                               "color": "black",
                               "background": "white",
                               "padding": "10px",
                               "border": "2px dashed black",
                               "borderRadius": "10px",
                               "boxShadow": f"0px 0px 0px 1px {'black'}",
                               "font-family":"Georgia"
                           })),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Tabs(
                                id="tabs2",
                                vertical = True,
                                children=[
                                    dcc.Tab(
                                        label="Selected Top Countries", 
                                        style={
                                            "background": "bisque",
                                            'color': 'black',
                                            'border': 'grey',
                                            'font-size': '15px',
                                            'align-items': 'center',
                                            'justify-content': 'center',
                                            'border-radius': '10px',
                                            'padding':'6px'
                                        },
                                        selected_style={
                                            "background": "black",
                                            'color': 'white',
                                            'border': 'grey',
                                            'font-size': '15px',
                                            'align-items': 'center',
                                            'justify-content': 'center',
                                            'border-radius': '10px',
                                            'padding':'6px'
                                        },
                                        children=[
                                            dcc.Loading(
                                                id="loading-box-plot1",
                                                children=[
                                                    html.Div(dcc.Graph(id="continent4-boxplot1",
                                                                       style = {"border": '1px solid white'}), 
                                                                       style={"float":'left'})
                                                    ],
                                                type="default"
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label="Remaining countries",
                                        style = {
                                            "background": "bisque",
                                            'color': 'black',
                                            'border': 'grey',
                                            'font-size': '15px',
                                            'align-items': 'center',
                                            'justify-content': 'center',
                                            'border-radius': '10px',
                                            'padding':'6px'
                                        },
                                        selected_style = {
                                            "background": "black",
                                            'color': 'white',
                                            'border': 'grey',
                                            'font-size': '15px',
                                            'align-items': 'center',
                                            'justify-content': 'center',
                                            'border-radius': '10px',
                                            'padding':'6px'
                                        },
                                        children=[
                                            dcc.Loading(
                                                id="loading-box-plot2",
                                                children=[
                                                    html.Div(dcc.Graph(id="continent4-boxplot2",
                                                                       style = {"border": '1px solid white'}), 
                                                                       style={"float":'left'})
                                                ],
                                                type="default"
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                    ),
                ]
            )
        ]
    ),
]
WORLDMAP_PLOT = dcc.Loading(
    id="world-map-plot", children=[dcc.Graph(id="worldmap")], type="default"
)
WORLDMAP = [
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([
                    WORLDMAP_PLOT
                ])
            ])
        ]
    )
]
BODY1 = html.Div(
    [
        dbc.Row(CONDITION, align="center", style={"marginTop": '10px', "width":'30%', "display": 'inline-block'}),
        dbc.Row(dbc.Col(dbc.Card(BAR)), style={"marginTop": '10px', "width":'68%', "float":'right', "display":'inline-block'}),
        dbc.Row(dbc.Card(GDP_HAPPINESS), style={"marginTop": '10px', "width":'68%', "float":'right', "display":'inline-block'}),
        dbc.Row(dbc.Card(BOXPLOT), style={"marginTop": '10px', "width":'68%', "float":'right', "display":'inline-block'})
    ]
)
BODY2 = dbc.Container(
    [
        dbc.Row(CONDITION2, align="center",
                style={"marginTop": 10}),
        dbc.Row([dbc.Col(dbc.Card(WORLDMAP))],
                style={"marginTop": 30})
   ]
)

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app_name = os.getenv("APP_NAME", "global-gdp")

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

index_page = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.H1(children="GLOBAL  GDP  ANALYSIS", 
                                style={"font-family":'Georgia',
                                       "color": 'navy'}), width=5),
                dbc.Col(width=5),
            ],
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H4(
                                children="""GDP stands for Gross Domestic Product. It is a key economic indicator that measures the monetary value of all final goods and services produced within a country's borders during a specific period, usually a year or a quarter.
                                          GDP is often used as a measure of a countrys economic performance and is used to compare the economic growth of different countries. It is calculated by adding up the total value of all goods and services produced within a country during a given period, including goods produced for domestic consumption and for export.""",
                            style = {"font-family":'Georgia',
                                     "color": 'gray'}
                            ),
                            html.Div(
                                [
                                    dcc.Link(
                                        html.Button(
                                            "HOME", id="home-button", className="mr-1",
                                            style = {
                                                "backgroundColor": 'black',
                                                "color": 'white',
                                                "font-family": 'Courier New',
                                                "font-size": '20px',
                                                "font-weight": 'bold',
                                                "border": '3px solid orange',
                                                "border-radius": '10px',
                                                "margin-right": '10px'
                                            }
                                        ),
                                        href=f"/{app_name}/",
                                    ),
                                    dcc.Link(
                                        html.Button(
                                            "WORLD MAP", id="worldmap-button", className="mr-1",
                                            style = {
                                                "backgroundColor": 'white',
                                                "color": 'black',
                                                "font-family": 'Courier New',
                                                "font-size": '20px',
                                                "font-weight": 'bold',
                                                "border": '3px solid orange',
                                                "border-radius": '10px',
                                                "margin-right": '10px'
                                            }
                                        ),
                                        href=f"/{app_name}/worldmap",
                                    ),
                                    dcc.Link(
                                        html.Button(
                                            "ANALYSIS", id="analysis-button", className="mr-1",
                                            style = {
                                                "backgroundColor": 'black',
                                                "color": 'white',
                                                "font-family": 'Courier New',
                                                "font-size": '20px',
                                                "font-weight": 'bold',
                                                "border": '3px solid orange',
                                                "border-radius": '10px',
                                                "margin-right": '10px'
                                            }
                                        ),
                                        href=f"/{app_name}/analysis"
                                    ),
                                ]
                            ),
                        ]
                    ),
                    width=7,
                ),
                dbc.Col(width=3),
            ],
            justify="center",
        ),
        html.Br(),
        dbc.Row(
            [dbc.Col(html.H4(children="WORLD MAP",
                             style = {"font-family":'Georgia'}), width=4), dbc.Col(width=4)],
            justify="center",
        ),
        html.Div(
            [
                dcc.Graph(
                    figure=px.choropleth(
                        merged,
                        locations="Country Code",
                        color="Country",
                        hover_name="Country"
                    )
                    .update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0},showlegend=False)
                )
            ],
            style={"display": "inline-block", "width": "90%"},
        ),
    ]
)

#WORLD MAP LAYOUT:

worldmap_layout = html.Div(
    [
        html.Div(id="worldmap-content"),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dcc.Link(
                                html.Button("HOME", id="home-button", className="mr-1",
                                            style = {
                                                "backgroundColor": 'black',
                                                "color": 'white',
                                                "font-family": 'Courier New',
                                                "font-size": '20px',
                                                "font-weight": 'bold',
                                                "border": '3px solid orange',
                                                "border-radius": '10px',
                                                "margin-right": '10px',
                                                "margin-top": "30px"
                                            }),
                                href=f"/{app_name}/",
                            ),
                            dcc.Link(
                                html.Button(
                                    "WORLD MAP", id="worldmap-button", className="mr-1",
                                    style = {
                                                "backgroundColor": 'white',
                                                "color": 'black',
                                                "font-family": 'Courier New',
                                                "font-size": '20px',
                                                "font-weight": 'bold',
                                                "border": '3px solid orange',
                                                "border-radius": '10px',
                                                "margin-right": '10px',
                                                "margin-top": "30px"
                                            }
                                ),
                                href=f"/{app_name}/worldmap",
                            ),
                            dcc.Link(
                                html.Button("ANALYSIS", id="analysis-button", className="mr-1",
                                            style = {
                                                "backgroundColor": 'black',
                                                "color": 'white',
                                                "font-family": 'Courier New',
                                                "font-size": '20px',
                                                "font-weight": 'bold',
                                                "border": '3px solid orange',
                                                "border-radius": '10px',
                                                "margin-right": '10px',
                                                "margin-top": "30px"
                                            }),
                                href=f"/{app_name}/analysis",
                            )
                        ]
                    ),
                    width=4,
                ),
                dbc.Col(width=7),
            ],
            justify="center",
        ),
        TITLE,
        dbc.Row(
            [
                dbc.Col(
                    html.H1("General picture of GDP worldwide",
                            style={"font-family":'Georgia'}), width=9
                ),
                dbc.Col(width=2),
            ],
            justify="center",
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    html.H5(children="""Global GDP, or the total economic output of all countries in the world, is a key indicator of the state of the global economy. 
                     It is influenced by factors such as population growth, technological advancements, natural resource availability, government policies, and international trade. 
                     The COVID-19 pandemic has had a significant impact on global GDP, with many countries experiencing a decline in economic activity due to lockdowns and restrictions on travel and commerce. 
                     However, there are signs of recovery in some parts of the world, particularly in countries that have successfully vaccinated their populations and reopened their economies. 
                     Overall, global GDP is expected to continue to grow in the coming years, albeit at a slower rate than before the pandemic.
                     The United States and China are two of the largest economies in the world, and their GDPs have a significant impact on global GDP. 
                     In recent years, China's GDP has been growing at a faster rate than that of the United States, and it is projected to become the world's largest economy by some measures in the coming years.""",
                    style = {
                        "font-family":'Georgia',
                        "color":'gray',
                        "margin-left":'10px',
                        "margin-right":'10px',
                        "margin-top":'10px',
                        "margin-bottom":'10px'
                    }
                    ),
                    style = {
                        "border" : '1px solid black',
                        "border-radius": '10px'
                    }
        ))),
        BODY2
    ]
)
@app.callback(
    Output("worldmap-content", "children"),
    Input("worldmap-button", "value")
)
@app.callback(
    Output('worldmap', 'figure'),
    Input('range-slider', 'value')
)
def update_worldmap(range_value):
    merged_sorted_filtered = merged_sorted[(merged_sorted['GDP'].between(range_value[0], range_value[1]))]
    fig = px.choropleth(merged_sorted_filtered,
                        locations="Country Code",
                        color="GDP",
                        color_continuous_scale="sunsetdark",
                        hover_name="Country",
                        hover_data=["Population"],
                        range_color=(merged['GDP'].min(), merged['GDP'].max()))
    fig.update_layout(title='<b>World Map Visualization - National GDP</b>', title_font=dict(size=25, color='red', family='Verdana'),
                      width=1400, height=700)
    return fig

#ANALYSIS LAYOUT:

analysis_layout = html.Div(
    [
        html.Div(id="analysis-content"),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dcc.Link(
                                html.Button("HOME", id="home-button", className="mr-1",
                                            style = {
                                                "backgroundColor": 'black',
                                                "color": 'white',
                                                "font-family": 'Courier New',
                                                "font-size": '20px',
                                                "font-weight": 'bold',
                                                "border": '3px solid orange',
                                                "border-radius": '10px',
                                                "margin-right": '10px',
                                                "margin-top": "15px"
                                            }),
                                href=f"/{app_name}/",
                            ),
                            dcc.Link(
                                html.Button(
                                    "WORLD MAP", id="worldmap-button", className="mr-1",
                                    style = {
                                                "backgroundColor": 'white',
                                                "color": 'black',
                                                "font-family": 'Courier New',
                                                "font-size": '20px',
                                                "font-weight": 'bold',
                                                "border": '3px solid orange',
                                                "border-radius": '10px',
                                                "margin-right": '10px',
                                                "margin-top": "15px"
                                            }
                                ),
                                href=f"/{app_name}/worldmap",
                            ),
                            dcc.Link(
                                html.Button("ANALYSIS", id="analysis-button", className="mr-1",
                                            style = {
                                                "backgroundColor": 'black',
                                                "color": 'white',
                                                "font-family": 'Courier New',
                                                "font-size": '20px',
                                                "font-weight": 'bold',
                                                "border": '3px solid orange',
                                                "border-radius": '10px',
                                                "margin-right": '10px',
                                                "margin-top": "15px"
                                            }),
                                href=f"/{app_name}/analysis",
                            )
                        ]
                    ),
                    width=4,
                ),
                dbc.Col(width=7),
            ],
            justify="center",
        ),
        TITLE,
        dbc.Row(
            [
                dbc.Col(
                    html.H1("Specific analysis of global GDP",
                            style={"font-family":'Georgia'}), width=9
                ),
                dbc.Col(width=2),
            ],
            justify="center",
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    html.H5(children="""The Happiness index, also known as the World Happiness Report, is an annual report that ranks countries based on their levels of happiness and well-being. 
                    The index is based on a variety of factors, including GDP per capita, social support, life expectancy, freedom to make life choices, generosity, and perceptions of corruption. 
                    The report is compiled by the United Nations Sustainable Development Solutions Network, and it provides policymakers with valuable insights into the factors that contribute to 
                    happiness and well-being in different countries around the world. The report has gained widespread attention in recent years, as policymakers and individuals alike seek to promote 
                    greater happiness and well-being in their communities. While the Happiness index is certainly not the only measure of well-being, it provides a valuable framework for understanding 
                    the factors that contribute to happiness and the steps that can be taken to promote well-being at both the individual and societal levels.""",
                    style = {
                        "font-family":'Georgia',
                        "color":'gray',
                        "margin-left":'10px',
                        "margin-right":'10px',
                        "margin-top":'10px',
                        "margin-bottom":'10px'
                    }
                    ),
                    style = {
                        "border" : '1px solid black',
                        "border-radius": '10px'
                    }
        ))),
        BODY1
    ]
)
@app.callback(
    Output("analysis-content", "children"),
    Input("analysis-button", "n_clicks")
)
def update_analysis_content(n_clicks):
    if n_clicks is None:
        return html.Div("Click on 'ANALYSIS' button to display the charts")
    else:
        return[
            dcc.Graph(id='continent3-treemap'),
            dcc.Graph(id='continent2-barchart'),
            dcc.Graph(id='continent1-scatter'),
            dcc.Graph(id='continent4-boxplot1'),
            dcc.Graph(id='continent4-boxplot2')
        ]
@app.callback(
        Output('continent3-treemap', 'figure'),
        Input('continent-drop', 'value')
)
def update_treemap(selected_region): 
    filtered_data1 = gdp[gdp['Continent'] == selected_region]
    fig = px.treemap(filtered_data1, path=['Continent','Country'], values='GDP', color='Happiness', color_continuous_scale='Rdbu', 
                 hover_data=['Population'], color_continuous_midpoint=np.average(gdp['Happiness'], weights=gdp['GDP']))
    fig.update_traces(textposition='middle center')
    fig.update_layout(title='<b>GDP and Happiness index</b>', title_font=dict(size=25, color='red', family='Verdana'),
                      height=450, width=1020, paper_bgcolor = 'whitesmoke')
    return fig
@app.callback(
    Output('continent2-barchart', 'figure'),
    [Input('continent-drop', 'value'),
     Input('selection-slider', 'value')]
)
def update_barchart(selected_region, selected_countries): 
    gdp_sorted = gdp.sort_values('GDP', ascending=False)
    filtered_data1 = gdp_sorted[gdp_sorted['Continent'] == selected_region][:selected_countries]
    fig = px.bar(filtered_data1, x='GDP', y='Country', color='Country', title='Top economies worldwide')
    fig.update_layout(
    title='<b>Top economies of selected continent</b>', title_font=dict(color='red', size=25, family='Verdana'),
    xaxis_tickfont_size=16,
    yaxis=dict(
        title='<b>Country</b>',
        titlefont_size=20,
        tickfont_size=12,
        color='navy'
    ),
    xaxis=dict(
        title='<b>Total GDP</b>',
        titlefont_size=20,
        tickfont_size=12,
        color='navy'
    ),
    bargap=0.3,
    plot_bgcolor='whitesmoke',
    showlegend=False,
    height = 550, width = 1020,
    paper_bgcolor = 'whitesmoke'
)
    return fig
@app.callback(
    Output('continent1-scatter', 'figure'),
    Input('continent-drop', 'value')
)
def update_scatter(selected_region): 
    gdp_sorted = gdp.sort_values('GDP', ascending=False)
    filtered_data2 = gdp_sorted[gdp_sorted['Continent'] == selected_region]
    fig = px.scatter(filtered_data2, x='Rank', y='Happiness', color='Development', hover_data=['GDP'], size='Happiness')
    fig.update_layout(
    title='<b>Happiness index and GDP Rank</b>',
    title_font=dict(color='red', size=25, family='Verdana'),
    yaxis=dict(
        title='<b>Hapiness index</b>',
        titlefont_size=20,
        color='navy',
        tickfont_size=12
    ),
    xaxis=dict(
        title='<b>GDP Rank</b>',
        titlefont_size=20,
        color='navy',
        tickfont_size=12
    ),
    legend=dict(
        font_size=13,
        font_color='black'
    ),
    plot_bgcolor='whitesmoke',
    height = 450, width = 1020,
    paper_bgcolor = 'whitesmoke'
)
    return fig
@app.callback(
    Output('continent4-boxplot1', 'figure'),
    Input('selection-slider', 'value')
)
def update_boxplot1(selected_countries): 
    gdp_sorted = gdp.sort_values('GDP', ascending=False)
    filtered_data3 = gdp_sorted[:selected_countries]
    fig = px.box(filtered_data3, y='GDP', x='Continent', color='Continent')
    fig.update_layout(
    title='<b>Distribution of GDP of selected top countries</b>', title_font=dict(color='red', size=25, family='Verdana'),
    xaxis_tickfont_size=16,
    yaxis=dict(
        title='<b>GDP</b>',
        titlefont_size=20,
        tickfont_size=12,
        color='navy'
    ),
    xaxis=dict(
        title='<b>Continent</b>',
        titlefont_size=20,
        tickfont_size=12,
        color='navy'
    ),
    plot_bgcolor='whitesmoke',
    height = 450, width = 940,
    paper_bgcolor = 'whitesmoke',
    showlegend = False
)
    return fig
@app.callback(
    Output('continent4-boxplot2', 'figure'),
    Input('selection-slider', 'value')
)
def update_boxplot2(selected_countries): 
    gdp_sorted = gdp.sort_values('GDP', ascending=False)
    filtered_data4 = gdp_sorted[selected_countries:]
    fig = px.box(filtered_data4, y='GDP', x='Continent', color='Continent')
    fig.update_layout(
    title='<b>Distribution of GDP of remaining countries</b>', title_font=dict(color='red', size=25, family='Verdana'),
    xaxis_tickfont_size=16,
    yaxis=dict(
        title='<b>GDP</b>',
        titlefont_size=20,
        tickfont_size=12,
        color='navy'
    ),
    xaxis=dict(
        title='<b>Continent</b>',
        titlefont_size=20,
        tickfont_size=12,
        color='navy'
    ),
    plot_bgcolor='whitesmoke',
    height = 450, width = 940,
    paper_bgcolor = 'whitesmoke',
    showlegend = False
)
    return fig

@app.callback(
        Output("page-content","children"),
        [Input("url","pathname")]
)
def display_page(pathname):
    if pathname.endswith("/worldmap"):
        return worldmap_layout
    elif pathname.endswith("/analysis"):
        return analysis_layout
    else:
        return index_page
if __name__ == '__main__':
    app.run(debug=True)
