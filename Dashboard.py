import pandas as pd
import numpy as np
from datetime import datetime
from math import log, e
from plotly import graph_objects as go
import plotly.express as px
import dash
import plotly.figure_factory as ff
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__)

my_css_url = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
my_css_url = "https://codepen.io/amyoshino/pen/jzXypZ.css"
app.css.append_css({
    "external_url": my_css_url
})

app.config['suppress_callback_exceptions'] = True

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
              "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
              "#08519c", "#0b4083", "#08306b"
              ]
### CLEANING OUT THE DATA ###

us_time_series = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")

us_time_series = us_time_series.drop(
    ["UID", "code3", "FIPS", "Lat", "Long_"], axis=1)

us_time_series = us_time_series.groupby('Province_State', as_index=False).sum()

new_columns = []
for col in us_time_series.columns:
    if col == "Province_State":
        new_columns.append("Province_State")
    else:
        mmddyyyy = col + "20"
        date_format = "%m/%d/%Y"
        current_date = datetime.strptime(mmddyyyy, date_format)
        original_date = datetime.strptime('1/22/2020', date_format)
        new_columns.append((current_date - original_date).days)

us_time_series.columns = new_columns

us_totals = us_time_series.drop(
    "Province_State", axis=1).sum(axis=0)[1:].to_list()

### APP LAYOUT ###

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='United States', value='tab-1'),
        dcc.Tab(label='Global', value='tab-2'),
    ]),
    html.Div(id='tab-content')
])

us_page = html.Div(children=[

    html.Div(className='row', children=[
        html.H1("COVID-19 Case Data for the United States",
                style={'text-align': 'center', 'margin-top': 40, 'margin-bottom':
                       10}),
    ]),

    html.Div(className='row', children=[
        html.H4("Made by Aarush Gupta and Shikhar Ahuja",
                style={'text-align': 'center', 'margin-top': 0, 'margin-bottom':
                       20}),
    ]),

    html.Hr(),

    html.Div(className='row', children=[

        html.Div(className="four columns", children=[
             html.Button('Switch Graph View',
                         id='line-graph-button', n_clicks=0)
             ], style={'margin-top': 30, 'text-align': 'center', 'color': 'white'}),

        html.Div(className="seven columns", children=[
            html.P("\nThis graph represents the number of cases of COVID-19 in the U.S. as a function of days after January 22, 2020. This data was collected by John Hopkins University and made freely available on GitHub. Toggle the button on the left to switch between graphs displaying data for states/provinces and totals for the United States. To view data only for a specific state, double-click its name in the legend of the graph. You can also compare the data of two or more states in this way as well.")
        ])

    ]),

    html.Div(className='row', children=[
        dcc.Graph(id='line_graph', config={'displayModeBar': False},
                  animate=True)
    ], style={'margin-left': 50, 'margin-right': 50}),

    html.Div(className='row', children=[
        html.P("The graph below plots the new daily cases versus the number of total cases at some point in time. Like for the graph above, click the button to toggle the graph data and click on a specific state to view its graph alone. Plotting the new cases versus total cases can help determine the type of growth of the curve. If points lie roughly along a straight line, this means that the number of new cases increases rapidly as the totals increase, which implies exponential growth. On the other hand, flat and declining curves imply constant and slowing growth, respectively. Due to the volatality of the graph, only a rough idea of the type of growth curve can be obtained.")
    ], style={'margin': 50}),

    html.Div(className='row', children=[
        dcc.Graph(id='line_graph_2', config={'displayModeBar': False},
                  animate=True)
    ], style={'margin-left': 50, 'margin-right': 50}),

    html.Div(className='row', children=[
        html.Div(className="eight columns", children=[
             dcc.Graph(id='map', style={"height": 500},
                       config={'displayModeBar': False})
             ]),
        html.Div(className="three columns", children=[
            html.P(
                 "This is a cloropleth map of COVID-19 cases in the United States. Note that the colors are scaled logarithmically so that differences are more visible. Move the slider below to change the day of the data the map is showing."),
            html.Div(className="row", children=[
                dcc.Slider(
                     id='day-slider',
                     min=0,
                     max=us_time_series.shape[1] - 3,
                     step=1,
                     value=us_time_series.shape[1] - 3,
                     ),
            ], style={"margin-top": 50})
        ], style={"margin-top": 150})
    ]),

    html.Div(className='row', children=[
        html.Div(children=[
             dcc.Graph(id='pie', config={'displayModeBar': False})
             ], className="six columns")
    ])
])

global_page = html.Div(children=[

    html.Div(className='row', children=[
        html.H1("Global COVID-19 Case Data",
                style={'text-align': 'center', 'margin-top': 40, 'margin-bottom':
                       10}),
    ]),

    html.Div(className='row', children=[
        html.H4("Made by Aarush Gupta and Shikhar Ahuja",
                style={'text-align': 'center', 'margin-top': 0, 'margin-bottom':
                       20}),
    ]),

    html.Hr(),

    html.Div(className='row', children=[

        html.Div(className="four columns", children=[
             html.Button('Switch Graph View',
                         id='line-graph-button', n_clicks=0)
             ], style={'margin-top': 30, 'text-align': 'center', 'color': 'white'}),

        html.Div(className="seven columns", children=[
            html.P("\nThis graph represents the number of cases of COVID-19 in the U.S. as a function of days after January 22, 2020. This data was collected by John Hopkins University and made freely available on GitHub. Toggle the button on the left to switch between graphs displaying data for states/provinces and totals for the United States. To view data only for a specific state, double-click its name in the legend of the graph. You can also compare the data of two or more states in this way as well.")
        ])

    ]),

    html.Div(className='row', children=[
        dcc.Graph(id='line_graph', config={'displayModeBar': False},
                  animate=True)
    ], style={'margin-left': 50, 'margin-right': 50}),

    html.Div(className='row', children=[
        html.P("The graph below plots the new daily cases versus the number of total cases at some point in time. Like for the graph above, click the button to toggle the graph data and click on a specific state to view its graph alone. Plotting the new cases versus total cases can help determine the type of growth of the curve. If points lie roughly along a straight line, this means that the number of new cases increases rapidly as the totals increase, which implies exponential growth. On the other hand, flat and declining curves imply constant and slowing growth, respectively. Due to the volatality of the graph, only a rough idea of the type of growth curve can be obtained.")
    ], style={'margin': 50}),

    html.Div(className='row', children=[
        dcc.Graph(id='line_graph_2', config={'displayModeBar': False},
                  animate=True)
    ], style={'margin-left': 50, 'margin-right': 50}),

    html.Div(className='row', children=[
        html.Div(className="eight columns", children=[
             dcc.Graph(id='map', style={"height": 500},
                       config={'displayModeBar': False})
             ]),
        html.Div(className="three columns", children=[
            html.P(
                 "This is a cloropleth map of COVID-19 cases in the United States. Note that the colors are scaled logarithmically so that differences are more visible. Move the slider below to change the day of the data the map is showing."),
            html.Div(className="row", children=[
                dcc.Slider(
                     id='day-slider',
                     min=0,
                     max=us_time_series.shape[1] - 3,
                     step=1,
                     value=us_time_series.shape[1] - 3,
                     ),
            ], style={"margin-top": 50})
        ], style={"margin-top": 150})
    ]),

    html.Div(className='row', children=[
        html.Div(children=[
             dcc.Graph(id='pie', config={'displayModeBar': False})
             ], className="six columns")
    ])
])

#### CALLBACKS ####


@app.callback(
    Output(component_id='tab-content', component_property='children'),
    [Input(component_id='tabs', component_property='value')]
)
def return_content(val):
    if val == 'tab-1':
        return us_page
    else:
        return global_page


@ app.callback(
    [Output(component_id='line_graph', component_property='figure'), Output(
        component_id='line_graph_2', component_property='figure')],
    [Input(component_id='line-graph-button', component_property='n_clicks')]
)
def display_line_graph(n_clicks):
    fig = go.Figure()
    fig2 = go.Figure()

    if n_clicks % 2 == 0:
        fig.add_trace(go.Scatter(x=np.arange(len(us_totals)),
                                 y=us_totals, mode='lines+markers', name='Cases in the US'))

        new_cases = []
        for i in range(len(us_totals)):
            if i == 0:
                new_cases.append(us_totals[0])
            else:
                new_cases.append(us_totals[i] - us_totals[i-1])

        fig2.add_trace(go.Scatter(x=us_totals,
                                  y=new_cases, mode='lines+markers', name='Cases in the US'))

        title1 = "Total COVID-19 Cases in the United States vs. Days since Jan. 20, 2022"
        title2 = "New COVID-19 Cases in the United States vs. Total Cases"
    else:
        for loc in us_time_series['Province_State'].to_list():
            y_list = us_time_series[us_time_series['Province_State'] == loc].transpose()[
                2:].squeeze().to_list()
            fig.add_trace(go.Scatter(x=np.arange(len(y_list)),
                                     y=y_list, mode='lines+markers', name=loc))

            new_cases = []
            for i in range(len(us_totals)):
                if i == 0:
                    new_cases.append(y_list[0])
                else:
                    new_cases.append(y_list[i] - y_list[i-1])

            fig2.add_trace(go.Scatter(x=y_list,
                                      y=new_cases, mode='lines+markers', name=loc))

        title1 = "COVID-19 Cases in States and Provinces"
        title2 = "New COVID-19 Cases vs. Total Cases in States and Provinces"

    fig.update_layout(title=title1,
                      xaxis_title='Days since Jan. 22, 2020',
                      yaxis_title='Number of Cases', template='plotly_dark', hovermode='x unified', hoverlabel=dict(
                          bgcolor="black",
                          font_size=11,
                          font_family="Rockwell",
                          font_color="white"
                      ))

    fig2.update_layout(title=title2,
                       xaxis_title='Number of Cases',
                       yaxis_title='Number of New Cases', template='plotly_dark', hovermode='x unified', hoverlabel=dict(
                           bgcolor="black",
                           font_size=11,
                           font_family="Rockwell",
                           font_color="white"
                       ))

    return fig, fig2


@ app.callback(
    [Output(component_id='map', component_property='figure'),
     Output(component_id='pie', component_property='figure')],
    [Input(component_id='day-slider', component_property='value')]


)
def display_map(slider_val):
    loc_cases = pd.DataFrame(
        columns=["Location", "Number of Cases", "Log Number of Cases"])
    for loc in us_time_series['Province_State']:
        if loc in us_state_abbrev.keys():
            log_val = log(us_time_series[us_time_series['Province_State'] == loc].transpose()[
                2:].squeeze().to_list()[slider_val])/log(10) if us_time_series[us_time_series['Province_State'] == loc].transpose()[
                2:].squeeze().to_list()[slider_val] != 0 else 0
            loc_cases = loc_cases.append(
                {"Location": us_state_abbrev[loc], "Number of Cases": us_time_series[us_time_series['Province_State'] == loc].transpose()[
                    2:].squeeze().to_list()[slider_val], "Log Number of Cases": log_val}, ignore_index=True)

    fig = go.Figure(data=go.Choropleth(
        locations=loc_cases['Location'],  # Spatial coordinates
        z=loc_cases['Log Number of Cases'].astype(
            float),  # Data to be color-coded
        locationmode='USA-states',
        colorbar=dict(len=1,
                      title='Number of Cases (Logarithmic)',
                      x=0.9,
                      tickvals=[0, 1, 2, 3, 4, 5, 6],
                      ticktext=['0', '10', '100', '1000', '10000', '100000', '1000000'])
    ),)

    fig.update_layout(
        title_text='Map of COVID-19 Cases in the U.S.',  # Create a Title
        geo_scope='usa',  # Plot only the USA instead of globe
        template='plotly_dark', hoverlabel=dict(
            bgcolor="white",
            font_size=11,
            font_family="Rockwell",
            font_color="white"
        )
    )

    loc_cases.loc[loc_cases['Number of Cases'] /
                  us_totals[slider_val] < 0.02, 'Location'] = 'Other'
    return fig, px.pie(loc_cases, values='Number of Cases', names='Location', template='plotly_dark', color_discrete_sequence=px.colors.sequential.Inferno)


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')
