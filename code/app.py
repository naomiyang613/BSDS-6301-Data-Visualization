import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from urllib.request import urlopen

import json

# Init
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "US Population Migration Visualizer"


state_to_short_code_mapping = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
    'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
    'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI',
    'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
    'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND',
    'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}

abbrev_to_state = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois',
    'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
    'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan',
    'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
    'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota',
    'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
    'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota',
    'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming'
}

# Load data
states_total_flow_data = pd.read_csv('data/state_totals_2023.csv')
states_flow_data_breakdown = pd.read_csv('data/state_to_state_flows_2023.csv')
states_total_flow_data['short_code'] = states_total_flow_data['state'].map(state_to_short_code_mapping)

def create_map():
    fig = go.Figure(data=go.Choropleth(
        locations=states_total_flow_data['short_code'],
        z=states_total_flow_data['net_migration'],
        locationmode='USA-states',
        zmid=0,
        text=states_total_flow_data['state'],
        showscale=False
    ))
    
    fig.update_layout(
        geo=dict(
            scope='usa',
            projection=go.layout.geo.Projection(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)',
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig

def get_state_stats(state_name):
    state_data = states_total_flow_data[states_total_flow_data['state'] == state_name]
    
    stats = state_data.iloc[0]
    
    # Top 10 origins
    origin_totals = {}
    for i in range(len(states_flow_data_breakdown)):
        row = states_flow_data_breakdown.iloc[i]
        if row['destination'] == state_name and row['origin'] != state_name:
            origin = row['origin']
            estimate = row['estimate']
            if origin in origin_totals:
                origin_totals[origin] += estimate
            else:
                origin_totals[origin] = estimate
    
    sorted_origins = sorted(origin_totals.items(), key=lambda x: x[1], reverse=True)
    top_origins = dict(sorted_origins[:10])
    
    # Top 10 destinations
    dest_totals = {}
    for i in range(len(states_flow_data_breakdown)):
        row = states_flow_data_breakdown.iloc[i]
        if row['origin'] == state_name and row['destination'] != state_name:
            dest = row['destination']
            estimate = row['estimate']
            if dest in dest_totals:
                dest_totals[dest] += estimate
            else:
                dest_totals[dest] = estimate
    
    sorted_dests = sorted(dest_totals.items(), key=lambda x: x[1], reverse=True)
    top_dests = dict(sorted_dests[:10])
    
    return stats, top_origins, top_dests

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("US Migration", className="text-white"),
                html.P("Click on a state to see details", className="text-white")
            ], style={'background': 'blue', 'padding': '20px'})
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='map', figure=create_map(), config={'displayModeBar': False})
        ], width=8),
        
        dbc.Col([
            html.Div([
                html.H2(id='state-title', children='Select a state', style={'color': 'blue'}),
                html.Div(id='state-numbers', children=[html.P('Click a state')]),
                html.H3('Top 10 Origins (Move from)'),
                html.Ol(id='top-origins', children=[html.Li('Click a state')]),
                html.H3('Top 10 Destinations (Move to)'),
                html.Ol(id='top-dests', children=[html.Li('Click a state')])
            ], style={'border': '1px solid black', 'padding': '15px', 'background': 'white'})
        ], width=4)
    ])
], fluid=True)

@app.callback(
    [Output('state-title', 'children'),
     Output('state-numbers', 'children'),
     Output('top-origins', 'children'),
     Output('top-dests', 'children')],
    Input('map', 'clickData')
)
def update_sidepanel(clickData):
    if clickData == None:
        title = 'Select a state'
        info = [html.P('Click on any state')]
        origins = [html.Li('Click a state')]
        dests = [html.Li('Click a state')]
        return title, info, origins, dests
    
    state_code = clickData['points'][0]['location']
    state_name = abbrev_to_state[state_code]
    
    stats, top_origins, top_dests = get_state_stats(state_name)
    
    inflow = int(stats['inflow'])
    outflow = int(stats['outflow'])
    net = int(stats['net_migration'])
    
    inflow_str = f"{inflow:,}"
    outflow_str = f"{outflow:,}"
    if net >= 0:
        net_str = f"+{net:,}"
    else:
        net_str = f"{net:,}"
    
    info = []
    info.append(html.Div([html.B('Inflow: '), inflow_str]))
    info.append(html.Div([html.B('Outflow: '), outflow_str]))
    info.append(html.Div([html.B('Net: '), net_str]))
    
    origins = []
    for origin in top_origins:
        estimate = int(top_origins[origin])
        text = origin + ' - ' + f"{estimate:,}"
        origins.append(html.Li(text))
    
    dests = []
    for dest in top_dests:
        estimate = int(top_dests[dest])
        text = dest + ' - ' + f"{estimate:,}"
        dests.append(html.Li(text))
    
    return state_name, info, origins, dests

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)
