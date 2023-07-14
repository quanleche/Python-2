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

gdp = pd.read_csv("D:\Foundation Year\Business IT 2\GDP Dataset.csv")
countryfile = "D:/Foundation Year/Business IT 2/shapefile/ne_110m_admin_0_countries.shp"
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
        'backgroundColor':'#002B36'
    },
    children=[
                dmc.Header(height = 35, fixed = False, pl=0, pr=0, pt=0, style={'background-color':'orange', 
                                                                                'color':'whitesmoke',
                                                                                'marginBottom':'30px',
                                                                                'marginTop':'-65px'},
                   children=[
                       dmc.Text("VIETNAMESE - GERMAN UNIVERSITY", 
                                style={'font-family':'Georgia', 
                                       'margin-left':10,
                                       'color':'black',
                                       'font-size':20,
                                       'padding': '5px'})
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
        "color": "#073642",
        "background": "#FDF6E3",
        "padding": "10px",
        "borderRadius": "10px",
        "font-family":"Georgia",
        "font-weight":'bold'
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
                "font-size": 15,
                "font-family":'Georgia',
                "background": '#002B36',
                "border-radius": '10px',
                "backgroundColor":'whitesmoke',
                "color":'black'
                },
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
            max=19400000,
            value=(10,20000000),
            marks={
                0:'0M',
                2000000:'2M', 
                4000000:'4M',
                6000000:'6M', 
                8000000:'8M', 
                10000000:'10M',
                12000000:'12M',
                14000000:'14M',
                16000000:'16M',
                18000000:'18M',
                19400000:'19.36M'
                }),
            style = {
            "margin-top": '30px',
            "margin-bottom": '15px',
            "color": '#FDF6E3'
            }
)
GDP_HAPPINESS = [
    dbc.CardHeader(html.H5("GDP and Happiness index",
                           style={
                               "fontSize": 20,
                               "textAlign": "center",
                               "color": "#FDF6E3",
                               "background": "#002B36",
                               "padding": "10px",
                               "borderRadius": "10px",
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
                                            'font-size': '20px',
                                            'font-family':'Georgia',
                                            'align-items': 'center',
                                            'justify-content': 'center',
                                            'border-radius': '10px',
                                            'padding':'6px'
                                        },
                                        selected_style={
                                            "background": "black",
                                            'color': 'white',
                                            'border': 'grey',
                                            'font-size': '20px',
                                            'font-family':'Georgia',
                                            'align-items': 'center',
                                            'justify-content': 'center',
                                            'border-radius': '10px',
                                            'padding':'6px'
                                        },
                                        children=[
                                            dcc.Loading(
                                                id="loading-treemap",
                                                children=[
                                                    html.Div(dcc.Graph(id="continent3-treemap"), 
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
                                            'font-size': '20px',
                                            'font-family':'Georgia',
                                            'align-items': 'center',
                                            'justify-content': 'center',
                                            'border-radius': '10px',
                                            'padding':'6px'
                                        },
                                        selected_style = {
                                            "background": "black",
                                            'color': 'white',
                                            'border': 'grey',
                                            'font-size': '20px',
                                            'font-family':'Georgia',
                                            'align-items': 'center',
                                            'justify-content': 'center',
                                            'border-radius': '10px',
                                            'padding':'6px'
                                        },
                                        children=[
                                            dcc.Loading(
                                                id="loading-scatter-plot",
                                                children=[
                                                    html.Div(dcc.Graph(id="continent1-scatter"), 
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
    id="loading-bar-plot", children=[dcc.Graph(id="continent2-barchart")], type="default"
)
BAR = [
    dbc.CardHeader(html.H5("Top countries of each continent",
                           style={
                               "fontSize": 20,
                               "textAlign": "center",
                               "color": "#FDF6E3",
                               "background": "#002B36",
                               "padding": "10px",
                               "borderRadius": "10px",
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
                               "color": "#FDF6E3",
                               "background": "#002B36",
                               "padding": "10px",
                               "borderRadius": "10px",
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
                                            'font-family': 'Georgia',
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
                                            'font-family': 'Georgia',
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
                                            'font-family':'Georgia',
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
                                            'font-family':'Georgia',
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
WORLDMAP_PLOT = dcc.Graph(figure={}, id='worldmap')
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
        dbc.Row(CONDITION, align="center", style={"marginTop": '150px',"marginLeft":'15px', "width":'40%', "height":'50%', "display": 'inline-block'}),
        dbc.Row(dbc.Col(dbc.Card(BAR)), style={"marginTop": '30px', "width":'60%', "height":'50%', "float":'right', "display":'inline-block'}),
        dbc.Row(dbc.Card(GDP_HAPPINESS), style={"marginTop": '10px', "width":'50%', "height":'50%', "float":'right', "display":'inline-block'}),
        dbc.Row(dbc.Card(BOXPLOT), style={"marginTop": '10px', "width":'50%', "height":'50%', "float":'left', "display":'inline-block'})
    ]
)
BODY2 = dbc.Container(
    [
        dbc.Row(CONDITION2, align="center",
                style={"marginTop": 10}),
        dbc.Row([dbc.Col(dbc.Card(WORLDMAP))],
                style={"marginTop": 30, "width": 1330, "height": 700})
    ]
)

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SOLAR])
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
                                       "color": 'white',
                                       "marginTop":'30px',
                                       'font-weight':'bold'}), width=5),
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
                                children="""GDP stands for Gross Domestic Product. GDP is often used as a measure of a country's economic performance and is used to 
                                compare the economic growth of different countries. It is calculated by adding up the total value of all goods and services produced within a country during a given period.""",
                            style = {"font-family":'Georgia',
                                     "color": '#FDF6E3', 
                                     "font-size": '15px',
                                     "marginTop":'20px',
                                     "backgroundColor":'#073642',
                                     "padding":'10px',
                                     "border-radius":'10px',
                                     "width":'1205px'}
                            ),
                            html.Div(
                            dbc.DropdownMenu(
                                [
                                    dcc.Link(
                                        html.Button(
                                            "HOME", id="home-button", className="mr-1",
                                            style = {
                                                "font-size":"15px", 
                                                "font-weight":"bold",
                                                "font-family":'Calibri',
                                                "marginLeft":"10px",
                                                "border-radius":'10px',
                                                "backgroundColor":'white',
                                                "color":'gray'
                                            }
                                        ),
                                        href=f"/{app_name}/",
                                    ),
                                    dcc.Link(
                                        html.Button(
                                            "WORLD MAP", id="worldmap-button", className="mr-1",
                                            style = {
                                                "font-size":"15px", 
                                                "font-weight":"bold",
                                                "font-family":'Calibri', 
                                                "marginLeft":"10px",
                                                "marginRight":'10px',
                                                "border-radius":'10px'
                                            }
                                        ),
                                        href=f"/{app_name}/worldmap",
                                    ),
                                    dcc.Link(
                                        html.Button(
                                            "ANALYSIS", id="analysis-button", className="mr-1",
                                            style = {
                                                "font-size":"15px", 
                                                "font-weight":"bold",
                                                "font-family":'Calibri', 
                                                "marginRight":"10px",
                                                "border-radius":'10px'
                                            }
                                        ),
                                        href=f"/{app_name}/analysis"
                                    ),
                                ],
                                nav=True,
								in_navbar=True,
								style = {"font-size":"20px", "font-weight":"bold", "marginTop":'20px', "font-family":'Calibri'},
								label="Menu"),
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
        html.Div(
            [
                dcc.Graph(
                    figure=px.choropleth(
                        merged,
                        locations="Country Code",
                        color="Country",
                        hover_name="Country"
                    )
                    .update_layout(height=600, margin={"r": 0, "t": 0, "l": 100, "b": 0},showlegend=False, plot_bgcolor='#002B36', paper_bgcolor='#002B36')
                )
            ],
            style={"display": "inline-block", 
                   "width": "90%",
                   "marginTop":'50px'},
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
                            dbc.DropdownMenu(
                                [
                                    dcc.Link(
                                        html.Button(
                                            "HOME", id="home-button", className="mr-1",
                                            style = {
                                                "font-size":"15px", 
                                                "font-weight":"bold",
                                                "font-family":'Calibri', 
                                                "marginLeft":"10px",
                                                "border-radius":'10px'
                                            }
                                        ),
                                        href=f"/{app_name}/",
                                    ),
                                    dcc.Link(
                                        html.Button(
                                            "WORLD MAP", id="worldmap-button", className="mr-1",
                                            style = {
                                                "font-size":"15px", 
                                                "font-weight":"bold",
                                                "font-family":'Calibri', 
                                                "marginLeft":"10px",
                                                "marginRight":'10px',
                                                "border-radius":'10px',
                                                "backgroundColor":'white',
                                                "color":'gray'
                                            }
                                        ),
                                        href=f"/{app_name}/worldmap",
                                    ),
                                    dcc.Link(
                                        html.Button(
                                            "ANALYSIS", id="analysis-button", className="mr-1",
                                            style = {
                                                "font-size":"15px", 
                                                "font-weight":"bold",
                                                "font-family":'Calibri', 
                                                "marginRight":"10px",
                                                "border-radius":'10px'
                                            }
                                        ),
                                        href=f"/{app_name}/analysis"
                                    ),
                                ],
                                nav=True,
								in_navbar=True,
								style = {"font-size":"20px", "font-weight":"bold", "marginTop":'35px', "marginLeft":'15px', "font-family":'Calibri'},
								label="Menu"),
                    ),
                ),
                dbc.Col(width=7),
            ],
            justify="center",
        ),
        TITLE,
        dbc.Row(
            [
                dbc.Col(
                    html.H1("General Picture of GDP Worldwide",
                            style={"font-family":'Georgia', "color":'white',"marginTop":'30px', "marginLeft":'-45px'}), width=9
                ),
                dbc.Col(width=2),
            ],
            justify="center",
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    html.H5(children="""Global GDP, or the total economic output of all countries in the world, is a key indicator of the state of the global economy.  
                     Overall, global GDP is expected to continue to grow in the coming years, albeit at a slower rate than before the pandemic.
                     The United States and China are two of the largest economies in the world, and their GDPs have a significant impact on global GDP. 
                     In recent years, China's GDP has been growing at a faster rate than that of the United States, and it is projected to become the world's largest economy by some measures in the coming years.""",
                    style = {
                        "font-family":'Georgia',
                        "font-size":'15px',
                        "color":'#FDF6E3',
                        "margin-left":'10px',
                        "margin-right":'10px',
                        "margin-top":'10px',
                        "margin-bottom":'10px'
                    }
                    ),
                    style = {
                        "border-radius": '10px',
                        "marginLeft": '15px',
                        "marginRight": '15px',
                        "padding": '3px',
                        "backgroundColor": '#073642'
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
    fig.update_layout(title='<b>NATIONAL  GDP</b>', title_font=dict(size=25, color='red', family='Georgia'), title_x=0.5, title_y=0.96,
                     width = 1270, height = 700)
    fig.add_annotation(text='Unit: million USD | Reference source: World Bank', font=dict(size=15, family='Georgia'), y=-0.1)
    return fig

#ANALYSIS LAYOUT:

analysis_layout = html.Div(
    [
        html.Div(id="analysis-content"),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                            dbc.DropdownMenu(
                                [
                                    dcc.Link(
                                        html.Button(
                                            "HOME", id="home-button", className="mr-1",
                                            style = {
                                                "font-size":"15px", 
                                                "font-weight":"bold",
                                                "font-family":'Calibri', 
                                                "marginLeft":"10px",
                                                "border-radius":'10px'
                                            }
                                        ),
                                        href=f"/{app_name}/",
                                    ),
                                    dcc.Link(
                                        html.Button(
                                            "WORLD MAP", id="worldmap-button", className="mr-1",
                                            style = {
                                                "font-size":"15px", 
                                                "font-weight":"bold",
                                                "font-family":'Calibri', 
                                                "marginLeft":"10px",
                                                "marginRight":'10px',
                                                "border-radius":'10px'
                                            }
                                        ),
                                        href=f"/{app_name}/worldmap",
                                    ),
                                    dcc.Link(
                                        html.Button(
                                            "ANALYSIS", id="analysis-button", className="mr-1",
                                            style = {
                                                "font-size":"15px", 
                                                "font-weight":"bold",
                                                "font-family":'Calibri', 
                                                "marginRight":"10px",
                                                "border-radius":'10px',
                                                "backgroundColor":'white',
                                                "color":'gray'
                                            }
                                        ),
                                        href=f"/{app_name}/analysis"
                                    ),
                                ],
                                nav=True,
								in_navbar=True,
								style = {"font-size":"20px", "font-weight":"bold","marginTop":'10px',"marginLeft":'-40px', "font-family":'Calibri'},
								label="Menu"),
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
                    html.H1("Specific Analysis of Global GDP",
                            style={"font-family":'Georgia', "color":'white', "marginTop":'30px', "marginLeft":'-45px'}), width=9
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
                    While the Happiness index is certainly not the only measure of well-being, it provides a valuable framework for understanding 
                    the factors that contribute to happiness and the steps that can be taken to promote well-being at both the individual and societal levels.""",
                    style = {
                        "font-family":'Georgia',
                        "font-size":'15px',
                        "color":'#FDF6E3',
                        "margin-left":'10px',
                        "margin-right":'10px',
                        "margin-top":'10px',
                        "margin-bottom":'10px'
                    }
                    ),
                    style = {
                        "padding": '5px',
                        "marginLeft": '15px',
                        "marginRight": '15px',
                        "backgroundColor": '#073642',
                        "border-radius":'10px'
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
        return html.Div(".")
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
    fig.update_layout(title='<b>GDP and Happiness index</b>', title_font=dict(size=20, color='red', family='Georgia'),
                      height=400, width=700, paper_bgcolor = 'whitesmoke', margin=dict(l=0, r=50, t=0, b=0))
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
    title='<b>Top economies of selected continent</b>', title_font=dict(color='red', size=20, family='Georgia'),
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
    height = 450, width = 860,
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
    title_font=dict(color='red', size=20, family='Georgia'),
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
    height = 400, width = 700,
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
    title='<b>Distribution of GDP of selected top countries</b>', title_font=dict(color='red', size=20, family='Georgia'),
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
    height = 440, width = 610,
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
    title='<b>Distribution of GDP of remaining countries</b>', title_font=dict(color='red', size=20, family='Georgia'),
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
    height = 440, width = 610,
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
