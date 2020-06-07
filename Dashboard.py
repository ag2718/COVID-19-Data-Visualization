
import pandas as pd
import numpy as np
from datetime import datetime

import plotly.graph_objects as go
import plotly.express as px
import dash
import plotly.figure_factory as ff
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

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

    html.Div([

        html.Div([
            html.H1("COVID-19 Case Data for the United States",
                    style={'text-align': 'center'}),
        ], className="row"),

        html.Div([
            html.Div([
                dcc.Dropdown(id='dropdown',
                             options=[{'label': 'Total', 'value': 'the United States'}, {
                                 'label': 'Individual', 'value': 'All Locations'}],
                             value="the United States"
                             ),
            ]),
            html.Div([
                dcc.Graph(id='line_graph'),
            ]),
            html.Div([
                html.P("\nThis graph represents the number of cases of COVID-19 in the U.S. as a function of days after January 22, 2020. This data was collected by John Hopkins University and made freely available on GitHub. Either select 'Total' to view all cases, or select 'Invidual to view individual data for all the states. To view data only for a specific state, click in the legend of the graph. You can also compare the data of two or more states in this way.")
            ])
        ], className="row"),

        html.Div([
            html.Div([
                dcc.Graph(id='map')
            ]),
            html.Div([
                dcc.Slider(
                    id='day-slider',
                    min=0,
                    max=len(us_time_series) - 2,
                    step=1,
                    value=len(us_time_series) - 2,
                ),
            ])
        ], className="row")
    ])
])


@app.callback(
    Output(component_id='line_graph', component_property='figure'),
    [Input(component_id='dropdown', component_property='value')]
)
def display_line_graph(val):
    fig = go.Figure()
    if val == "the United States":
        fig.add_trace(go.Scatter(x=np.arange(len(us_totals)),
                                 y=us_totals, mode='lines+markers', name='Cases in the US'))
    elif val == "All Locations":
        for loc in us_time_series['Province_State'].to_list():
            y_list = us_time_series[us_time_series['Province_State'] == loc].transpose()[
                2:].squeeze().to_list()
            fig.add_trace(go.Scatter(x=np.arange(len(y_list)),
                                     y=y_list, mode='lines+markers', name=f'{loc}'))

    fig.update_layout(title=f'COVID-19 Cases in {val}',
                      xaxis_title='Days since Jan. 22, 2020',
                      yaxis_title='Number of Cases', template='plotly_white', hovermode='x unified', hoverlabel=dict(
                          bgcolor="white",
                          font_size=11,
                          font_family="Rockwell"
                      ))
    return fig


@app.callback(
    Output(component_id='map', component_property='figure'),
    [Input(component_id='day-slider', component_property='value')]
)
def display_map(slider_val):
    loc_cases = pd.DataFrame(columns=["Location", "Number of Cases"])
    for loc in us_time_series['Province_State']:
        if loc in us_state_abbrev.keys():
            loc_cases = loc_cases.append({"Location": us_state_abbrev[loc], "Number of Cases": us_time_series[us_time_series['Province_State'] == loc].transpose()[
                2:].squeeze().to_list()[slider_val]}, ignore_index=True)

    """ fig = px.choropleth(loc_cases,  # Input Pandas DataFrame
                        locations="Location",  # DataFrame column with locations
                        color="Number of Cases",
                        range_color=(0, 12),
                        color_continuous_scale="Viridis",  # DataFrame column with color values
                        hover_name="Number of Cases",  # DataFrame column hover info
                        locationmode='USA-states')  # Set to plot as US States """

    fig = go.Figure(data=go.Choropleth(
        locations=loc_cases['Location'],  # Spatial coordinates
        z=loc_cases['Number of Cases'].astype(
            float),  # Data to be color-coded
        locationmode='USA-states',  # set of locations match entries in `   s`
        colorscale='Reds',
        colorbar_title="Number of Cases",
    ))

    print(loc_cases['Location'])
    print(loc_cases['Number of Cases'])

    fig.update_layout(
        title_text='Map of COVID-19 Cases in the U.S.',  # Create a Title
        geo_scope='usa',  # Plot only the USA instead of globe
    )
    return fig

    """     print(loc_cases)

    fig = ff.create_choropleth(fips=loc_cases["Location"], values=loc_cases["Number of Cases"], colorscale=colorscale,
                               county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, round_legend_values=True,
                               legend_title='Number of Cases', title='US Map of COVID-19 Cases'
                               ) """


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')
