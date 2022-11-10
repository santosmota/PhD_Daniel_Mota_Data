import pathlib
from dash import Dash, html, dcc, ctx
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output
import pandas as pd

#########################
# deployment
# https://www.youtube.com/watch?v=Gv910_b5ID0


##########################
# this does not seem to work
load_figure_template('VAPOR')   # LUX DARKLY CYBORG
# https://towardsdatascience.com/3-easy-ways-to-make-your-dash-application-look-better-3e4cfefaf772

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("assets").resolve()
df1 = pd.read_csv(DATA_PATH.joinpath('RawData_Case1.csv'))
df2 = pd.read_csv(DATA_PATH.joinpath('RawData_Case2.csv'))
df3 = pd.read_csv(DATA_PATH.joinpath('RawData_Case3.csv'))

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

#######################
# GAUGES
gauge_size = 180
gauge_label_font_size = '20px'
gauge_units_font_size = '10px'
gauge_bar_color = 'white'
gauge_label_pos = 'bottom'

##########################
# the theme does not really become dark
app = Dash(__name__,
           title='Power Reserves',
           external_stylesheets=[dbc.themes.VAPOR])  # dbc.themes.LUX   SANDSTONE


##########################
# LAYOUT
app.layout = html.Div(children=[

    ##########################
    dbc.Row([
        ######################
        dbc.Col([
            daq.Gauge(
                id='governor',
                size=gauge_size,
                # color={'gradient': True,"ranges":{"green":[0,50],"yellow":[50,55],"red":[55,60]}},
                color={'gradient': False, "ranges": {gauge_bar_color: [0, 60]}},
                scale={'start': 0, 'interval': 5, 'labelInterval': 1},
                label={'label': 'Gas Turbines (MW)', 'style': {'font-size': gauge_label_font_size}},
                showCurrentValue=True,
                value=32,
                # units='MW',
                max=60,
                min=0,
                labelPosition=gauge_label_pos,
            ),
            daq.Gauge(
                id='fuelcell',
                size=gauge_size,
                # color={'gradient': True, "ranges": {"green": [0, 6], "yellow": [6, 7], "red": [7, 8]}},
                color={'gradient': False, "ranges": {gauge_bar_color: [0, 8]}},
                scale={'start': 0, 'interval': 1, 'labelInterval': 1},
                label={'label': 'Fuel Cell (MW)', 'style': {'font-size': gauge_label_font_size}},
                showCurrentValue=True,
                value=0,
                # units='MW',
                max=8,
                min=0,
                labelPosition=gauge_label_pos,
            ),
        ]),
        ######################
        dbc.Col([
            daq.Gauge(
                id='frequency',
                size=gauge_size,
                color={'gradient': True, "ranges": {gauge_bar_color: [47,53]}},
                scale={#'start': 47, 'interval': 0.5, 'labelInterval': 2,
                    'custom': {# 45: '45',
                                  # 46: '46',
                                  47: '47',
                                  48: '48',
                                  49: '49',
                                  50: '50',
                                  51: '51',
                                  52: '52',
                                  53: '53',
                                  # 54: '54',
                                  # 55: '55',
                                  }},
                label={'label': 'Frequency (Hz)', 'style': {'font-size': gauge_label_font_size}},
                showCurrentValue=True,
                value=50,
                # units='Hz',
                max=53,
                min=47,
                labelPosition=gauge_label_pos,
            ),
            daq.Gauge(
                id='inertia',
                size=gauge_size,
                color={'gradient': True, "ranges": {gauge_bar_color: [-14, 14]}},
                label={'label': 'Inertial Power (MW)', 'style': {'font-size': gauge_label_font_size}},
                showCurrentValue=True,
                scale={'start': -14, 'interval': 1, 'labelInterval': 2},
                value=0,
                # units='MW',
                max=14,
                min=-14,
                labelPosition=gauge_label_pos,
            ),
        ]),
        ######################
        dbc.Col([
            daq.Gauge(
                id='load',
                size=gauge_size,
                color={'gradient': False, "ranges": {gauge_bar_color: [0, 60]}},
                scale={'start': 0, 'interval': 5, 'labelInterval': 1},
                label={'label': 'Load (MW)', 'style': {'font-size': gauge_label_font_size}},
                showCurrentValue=True,
                value=44,
                # units='MW',
                max=60,
                min=0,
                labelPosition=gauge_label_pos,
            ),
            daq.Gauge(
                id='battery',
                size=gauge_size,
                color={'gradient': True, "ranges": {gauge_bar_color: [-4, 4]}},
                scale={'start': -4, 'interval': 1, 'labelInterval': 1},
                label={'label': 'Battery (MW)', 'style': {'font-size': gauge_label_font_size}},
                showCurrentValue=True,
                value=0,
                # units='MW',
                max=4,
                min=-4,
                labelPosition=gauge_label_pos,
            )
        ]),
        ######################
        dbc.Col([
            daq.Gauge(
                id='wind',
                size=gauge_size,
                color={'gradient': False, "ranges": {gauge_bar_color: [0, 14]}},
                scale={'start': 0, 'interval': 1, 'labelInterval': 1},
                label={'label': 'Wind Farm (MW)', 'style': {'font-size': gauge_label_font_size}},
                showCurrentValue=True,
                value=12,
                # units='MW',
                max=14,
                min=0,
                labelPosition=gauge_label_pos,
            ),
            daq.Gauge(
                id='soc',
                size=gauge_size,
                color={'gradient': False, "ranges": {gauge_bar_color: [0, 80]}},
                scale={'start': 0, 'interval': 10, 'labelInterval': 1},
                label={'label': 'SOC (kWh)', 'style': {'font-size': gauge_label_font_size}},
                showCurrentValue=True,
                value=75,
                # units='kWh',
                max=80,
                min=0,
                labelPosition=gauge_label_pos,
            )
        ]),
        dbc.Col(
            html.Img(id='grafico',
                     src=r'assets/Case1.png', # DATA_PATH.joinpath('Case1.png'),
                     alt='image',
                     style={'width': '300px',
                            'margin-top': '10px',
                            'margin-right': '10px'})
        )
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
            value=9,
            marks=dict_slider_marks,
            tooltip={"placement": "bottom", "always_visible": True}
        )
    ),

    ##########################
    dbc.Row([
        dbc.Col([
            html.Label('Select case:'),
            dcc.Dropdown(['Case 1', 'Case 2', 'Case 3'], 'Case 1', id='case')
        ], width=2)
    ], style={'margin-top': '10px'})

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
#     Output('grafico', 'src'),
    Input('time_slider', 'value'),
    Input('case', 'value')
)
def update_output(slider_value, case_value):

    idx = int(slider_value * time_to_samples)

    val = {}
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
        val['Pgov'] = df1['Pgov'].iloc[idx]
        val['F'] = df1['F'].iloc[idx]
        val['Pinert'] = df1['Pinert'].iloc[idx]
        val['Pbat'] = df1['Pbat'].iloc[idx]
        val['Pload'] = df1['Pload'].iloc[idx]
        val['Pfc'] = df1['Pfc'].iloc[idx]
        val['Pwf'] = df1['Pwf'].iloc[idx]
        val['SOC'] = df1['SOC'].iloc[idx]

    return val['Pgov'], val['F'], val['Pload'], val['Pwf'], val['Pinert'], val['Pbat'], val['SOC'], val['Pfc']


################################
# CASE VALUE AND CHART WITH TRANSIENTS
@app.callback(
    Output('grafico', 'src'),
    Input('case', 'value')
)
def update_output(case_value):

    if case_value == 'Case 2':
        filename = r'assets/Case2.png'
        # filename = DATA_PATH.joinpath('Case2.png').as_posix()

    elif case_value == 'Case 3':
        filename = r'assets/Case3.png'

    else:
        filename = r'assets/Case1.png'

    return filename




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
