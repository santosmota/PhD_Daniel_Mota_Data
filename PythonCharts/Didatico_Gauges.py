from dash import Dash, html, dcc, ctx
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output
import pandas as pd

##########################
# this does not seem to work
load_figure_template('BOOTSTRAP')   #
# https://towardsdatascience.com/3-easy-ways-to-make-your-dash-application-look-better-3e4cfefaf772

#######################
filename = '..\Modelos\Didatico\RawData_Case2.csv'
df2 = pd.read_csv(filepath_or_buffer=filename)

#######################
filename = '..\Modelos\Didatico\RawData_Case3.csv'
df3 = pd.read_csv(filepath_or_buffer=filename)

#######################
# Slider time and samples
Tstart = 0
Tend = 120
Tstep = 10

Ts = 0.005
time_to_samples = 1.0 / Ts

#gfx = ((1.0 - 0.5) / 4.0) / 2
#gfy = ((1.0 - 0.45) / 3.0) / 2

dict_slider_marks = {}
for t in range(Tstart, Tend, Tstep):
    dict_slider_marks[int(t)] = str(t)




##########################
# the theme does not really become dark
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # dbc.themes.LUX   SANDSTONE


##########################
# LAYOUT
app.layout = html.Div(children=[
    ##########################
    dbc.Row([
        ######################
        dbc.Col([
            daq.Gauge(
                id='governor',
                # color={'gradient': True,"ranges":{"green":[0,40],"yellow":[40,50],"red":[50,60]}},
                color={"ranges": {"gray": [0, 60]}},
                label='GTs',
                showCurrentValue=True,
                value=32,
                units='MW',
                max=60,
                min=0,
                labelPosition='top',
            ),
            daq.Gauge(
                id='fuelcell',
                color={"ranges": {"gray": [0, 8]}},
                label='Fuel Cell',
                showCurrentValue=True,
                value=0,
                units='MW',
                max=8,
                min=0,
                labelPosition='top',
            ),
        ]),
        ######################
        dbc.Col([
            daq.Gauge(
                id='frequency',
                color={"ranges": {"gray": [45, 55]}},
                label='Frequency',
                showCurrentValue=True,
                value=50,
                units='Hz',
                max=55,
                min=45,
                labelPosition='top',
            ),
            daq.Gauge(
                id='inertia',
                color={"ranges": {"gray": [-14, 14]}},
                label='Inertial Power',
                showCurrentValue=True,
                value=0,
                units='MW',
                max=14,
                min=-14,
                labelPosition='top',
            ),
        ]),
        ######################
        dbc.Col([
            daq.Gauge(
                id='load',
                color={"ranges": {"gray": [0, 60]}},
                label='Load',
                showCurrentValue=True,
                value=44,
                units='MW',
                max=60,
                min=0,
                labelPosition='top',
            ),
            daq.Gauge(
                id='battery',
                color={"ranges": {"gray": [-4, 4]}},
                label='Battery',
                showCurrentValue=True,
                value=0,
                units='MW',
                max=4,
                min=-4,
                labelPosition='top',
            )
        ]),
        ######################
        dbc.Col([
            daq.Gauge(
                id='wind',
                color={"ranges": {"gray": [0, 14]}},
                label='Wind Farm',
                showCurrentValue=True,
                value=12,
                units='MW',
                max=14,
                min=0,
                labelPosition='top',
            ),
            daq.Gauge(
                id='soc',
                color={"ranges": {"gray": [0, 80]}},
                label='SOC',
                showCurrentValue=True,
                value=75,
                units='kWh',
                max=80,
                min=0,
                labelPosition='top',
            )
        ])
    ]),  # row # 'margin-left':'7px',  # style={'margin-top': '10px'}

    ##########################
    # dbc.Row([
    #     dbc.Col([
    #
    #     ])

    # ]),

    ##########################
    dbc.Row([
        dbc.Col(
            html.Label(
                'Time (s):',
                ), width=1,
        ),
        dbc.Col([
            html.Button('<', id='but_down', n_clicks=0),
            html.Button('>', id='but_up', n_clicks=0),
        ], width=1)
    ]),

    ##########################
    dbc.Row(
        dcc.Slider(
            id='time_slider',
            min=Tstart,
            max=Tend,
            step=1,
            value=0,
            marks=dict_slider_marks,
            tooltip={"placement": "bottom", "always_visible": True}
        )
    ),

    ##########################
    dbc.Row([
        dbc.Col([
            html.Label('Select case:'),
            dcc.Dropdown(['Case 1', 'Case 2', 'Case 3'], 'Case 2', id='case')
        ])
    ])

])


@app.callback(
    Output('governor', 'value'),
    Output('frequency', 'value'),
    Output('load', 'value'),
    Output('wind', 'value'),
    Output('inertia', 'value'),
    Output('battery', 'value'),
    Output('soc', 'value'),
    Output('fuelcell', 'value'),
    Input('time_slider', 'value'))
def update_output(slider_value):
    idx = int(slider_value * time_to_samples)

    val = {}
    case_value = 'Case 2'
    if case_value == 'Case 2':
        val['Pgov'] = df2['Pgov'].iloc[idx]
        val['F'] = df2['F'].iloc[idx]
        val['Pinert'] = df2['Pinert'].iloc[idx]
        val['Pbat'] = df2['Pbat'].iloc[idx]
        val['Pload'] = df2['Pload'].iloc[idx]
        val['Pfc'] = df2['Pfc'].iloc[idx]
        val['Pwf'] = df2['Pwf'].iloc[idx]
        val['SOC'] = df2['SOC'].iloc[idx]
    elif case_value == 'Case 3':
        val['Pgov'] = df3['Pgov'].iloc[idx]
        val['F'] = df3['F'].iloc[idx]
        val['Pinert'] = df3['Pinert'].iloc[idx]
        val['Pbat'] = df3['Pbat'].iloc[idx]
        val['Pload'] = df3['Pload'].iloc[idx]
        val['Pfc'] = df3['Pfc'].iloc[idx]
        val['Pwf'] = df3['Pwf'].iloc[idx]
        val['SOC'] = df3['SOC'].iloc[idx]
    else:
        val['Pgov'] = df2['Pgov'].iloc[idx]
        val['F'] = df2['F'].iloc[idx]
        val['Pinert'] = df2['Pinert'].iloc[idx]
        val['Pbat'] = df2['Pbat'].iloc[idx]
        val['Pload'] = df2['Pload'].iloc[idx]
        val['Pfc'] = df2['Pfc'].iloc[idx]
        val['Pwf'] = df2['Pwf'].iloc[idx]
        val['SOC'] = df2['SOC'].iloc[idx]

    return val['Pgov'], val['F'], val['Pload'], val['Pwf'], val['Pinert'], val['Pbat'], val['SOC'], val['Pfc']



################################
# SLIDER UP / DOWN
@app.callback(
    Output('time_slider', 'value'),
    Input('time_slider', 'value'),
    Input('but_up', 'n_clicks'),
    Input('but_down', 'n_clicks')
)
def up_slider(value, up, down):
    if ctx.triggered_id == 'but_up':
        aux = value + 1
        if aux < Tend - 1:
            return aux

    if ctx.triggered_id == 'but_down':
        aux = value - 1
        if aux >= 0:
            return aux

    return value




if __name__ == '__main__':
    app.run_server(debug=True, port=9004)
