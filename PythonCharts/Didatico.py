import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, ctx, Input, Output
import dash_daq as daq
# from dash import html
#from dash.dependencies import Input, Output

import pandas as pd


#######################
filename = '..\Modelos\Didatico\RawData_Case1.csv'
df1 = pd.read_csv(filepath_or_buffer=filename)

#######################
filename = '..\Modelos\Didatico\RawData_Case2.csv'
df2 = pd.read_csv(filepath_or_buffer=filename)

#######################
filename = '..\Modelos\Didatico\RawData_Case3.csv'
df3 = pd.read_csv(filepath_or_buffer=filename)



Tstart = 0
Tend = 120
Tstep = 10

Ts = 0.005
time_to_samples = 1.0 / Ts

gfx = ((1.0 - 0.5) / 4.0) / 2
gfy = ((1.0 - 0.45) / 3.0) / 2

needlecolor = 'purple'

dict_slider_marks = {}
for t in range(Tstart, Tend, Tstep):
    dict_slider_marks[int(t)] = str(t)

fig = go.Figure()


fig.add_trace(go.Indicator(
    name="governor",
    domain={'x': [1 / 8 - gfx, 1 / 8 + gfx], 'y': [0.5 - gfy, 0.5 + gfy]},
    value=32,
    number={'suffix': 'MW'},
    mode="gauge+number+delta",
    delta={'reference': 32},
    title={'text': "Gas Turbines"},
    gauge={'axis': {'range': [0, 60]},
           'bar': {'color': 'white'},
           'threshold': {'line': {'color': needlecolor, 'width': 4},
                         'thickness': 0.75, 'value': 32}}))

# fig.add_trace(daq.Gauge(
#     id="governor",
#     # domain={'x': [1 / 8 - gfx, 1 / 8 + gfx], 'y': [0.5 - gfy, 0.5 + gfy]},
#     value=32,
#     # number={'suffix': 'MW'},
#     #mode="gauge+number+delta",
#     #delta={'reference': 32},
#     # title={'text': "Gas Turbines"},
#     # gauge={'axis': {'range': [0, 60]},
#     #        'bar': {'color': 'white'},
#     #        'threshold': {'line': {'color': needlecolor, 'width': 4},
#     #                      'thickness': 0.75, 'value': 32}}))
# ))

fig.add_trace(go.Indicator(
    name="frequency",
    domain={'x': [3/8 - gfx, 3/8 + gfx], 'y': [0.5 - gfy, 0.5 + gfy]},
    value=50,
    number={'suffix': 'Hz'},
    mode="gauge+number+delta",
    title={'text': "Frequency"},
    delta={'reference': 50},
    gauge={'axis': {'range': [46, 54]},
           'bar': {'color': 'white'},
           #'steps': [
           #    {'range': [40, 49], 'color': "lightgray"},
           #    {'range': [51, 60], 'color': "gray"}],
           'threshold': {'line': {'color': needlecolor, 'width': 4},
                         'thickness': 0.75, 'value': 50}}))

fig.add_trace(go.Indicator(
    name="inertia",
    domain={'x': [3/8 - gfx, 3/8 + gfx], 'y': [1/6 - gfy, 1/6 + gfy]},
    value=0,
    number={'suffix': 'MW'},
    mode="gauge+number+delta",
    title={'text': 'Inertial Power'},
    delta={'reference': 0},
    gauge={'axis': {'range': [-12, 12]},
           'bar': {'color': 'white'},
           'threshold': {'line': {'color': needlecolor, 'width': 4},
                         'thickness': 0.75, 'value': 0}}))

fig.add_trace(go.Indicator(
    name="load",
    domain={'x': [5 / 8 - gfx, 5 / 8 + gfx], 'y': [5/6 - gfy, 5/6 + gfy]},
    value=32,
    number={'suffix':'MW'},
    mode="gauge+number+delta",
    delta={'reference': 44},
    title={'text': "Load"},
    gauge={'axis': {'range': [0, 60]},
           'bar': {'color': 'white'},
           'threshold': {'line': {'color': needlecolor, 'width': 4},
                         'thickness': 0.75, 'value': 44}}))

fig.add_trace(go.Indicator(
    name="battery",
    domain={'x': [5 / 8 - gfx, 5 / 8 + gfx], 'y': [0.5 - gfy, 0.5 + gfy]},
    value=0,
    number={'suffix': 'MW'},
    mode="gauge+number+delta",
    delta={'reference': 0},
    title={'text': "Battery"},
    gauge={'axis': {'range': [-4, 4]},
           'bar': {'color': 'white'},
           'threshold': {'line': {'color': needlecolor, 'width': 4},
                         'thickness': 0.75, 'value': 0}}))

fig.add_trace(go.Indicator(
    name="fuelcell",
    domain={'x': [5 / 8 - gfx, 5 / 8 + gfx], 'y': [1 / 6 - gfy, 1 / 6 + gfy]},
    value=0,
    number={'suffix':'MW'},
    mode="gauge+number+delta",
    delta={'reference': 0},
    title={'text': "Fuel Cell"},
    gauge={'axis': {'range': [0, 7]},
           'bar': {'color': 'white'},
           'threshold': {'line': {'color': needlecolor, 'width': 4},
                         'thickness': 0.75, 'value': 0}}))

fig.add_trace(go.Indicator(
    name="wind",
    domain={'x': [7 / 8 - gfx, 7 / 8 + gfx], 'y': [5/6 - gfy, 5/6 + gfy]},
    value=12,
    number={'suffix':'MW'},
    mode="gauge+number+delta",
    delta={'reference': 12},
    title={'text': "Wind Farm"},
    gauge={'axis': {'range': [0, 14]},
           'bar': {'color': 'white'},
           'threshold': {'line': {'color': needlecolor, 'width': 4},
                         'thickness': 0.75, 'value': 12}}))

fig.add_trace(go.Indicator(
    name="soc",
    domain={'x': [7 / 8 - gfx, 7 / 8 + gfx], 'y': [0.5 - gfy, 0.5 + gfy]},
    value=45,
    number={'suffix': 'kWh'},
    mode="gauge+number+delta",
    delta={'reference': 45},
    title={'text': "SOC"},
    gauge={'axis': {'range': [0, 80]},
           'bar': {'color': 'white'},
           'threshold': {'line': {'color': needlecolor, 'width': 4},
                         'thickness': 0.75, 'value': 45}}))



fig.update_layout(dict1={'height': 600})

# fig.update_layout(
#     font_family="Courier New",
#     font_color="blue",
#     title_font_family="Times New Roman",
#     title_font_color="red",
#     legend_title_font_color="green"
# )
# fig.update_xaxes(title_font_family="Arial")

app = dash.Dash(__name__)

app.layout = html.Div(children=[

    # html.H1(children='Power Reserves', style={'textAlign': 'center'}), # , 'color': '#7FDBFF'

    html.Label('Select case:'),
    dcc.Dropdown(['Case 1', 'Case 2', 'Case 3'], 'Case 2', id='case'),
    # html.Div(id='dd-output-container'),

    html.Div([dcc.Graph(figure=fig, id="frequency")]),

    html.Label('Time (s):'),
    html.Button('<', id='but_down', n_clicks=0),
    html.Button('>', id='but_up', n_clicks=0),
    html.Div([dcc.Slider(id='time_slider',
                         min=Tstart,
                         max=Tend,
                         step=1,
                         value=0,
                         marks=dict_slider_marks,
                         tooltip={"placement": "bottom", "always_visible": True}
                         )
              ])

]) # , style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(
    Output('frequency', 'figure'),
    Input('time_slider', 'value'),
    Input('case', 'value'),
)
def update_gauge(slider_value, case_value):

    idx = int(slider_value * time_to_samples)

    val = {}
    # aux = True
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

    gt = {'threshold': {'value': val['Pgov']}}
    fr = {'threshold': {'value': val['F']}}
    bt = {'threshold': {'value': val['Pbat']}}
    inert = {'threshold': {'value': val['Pinert']}}
    fc = {'threshold': {'value': val['Pfc']}}
    ld = {'threshold': {'value': val['Pload']}}
    soc = {'threshold': {'value': val['SOC']}}
    wf = {'threshold': {'value': val['Pwf']}}

    fig.update_traces(value=val['Pgov'], gauge=gt, selector=dict(name="governor"))
    fig.update_traces(value=val['F'], gauge=fr, selector=dict(name="frequency"))
    fig.update_traces(value=val['Pbat'], gauge=bt, selector=dict(name="battery"))
    fig.update_traces(value=val['Pload'], gauge=ld, selector=dict(name="load"))
    fig.update_traces(value=val['Pinert'], gauge=inert, selector=dict(name="inertia"))
    fig.update_traces(value=val['Pfc'], gauge=fc, selector=dict(name="fuelcell"))
    fig.update_traces(value=val['Pwf'], gauge=wf, selector=dict(name="wind"))
    fig.update_traces(value=val['SOC'], gauge=soc, selector=dict(name="soc"))

    return fig


################################
# SLIDER UP / DOWN
@app.callback(
    Output('time_slider', 'value'),
    Input('time_slider', 'value'),
    # Input('but_up', 'n_clicks_timestamp'),
    # Input('but_down', 'n_clicks_timestamp')
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

#################################
# MAIN
if __name__ == "__main__":
    app.run_server(debug=True)





# import plotly.graph_objects as go
# import plotly.express as px
# import pandas as pd
#
#
# def sliders_buttons():
#
#     filename = '..\Modelos\Didatico\RawData_Case2.csv'
#     df = pd.read_csv(filepath_or_buffer=filename)
#
#     fig = px.scatter(df, x='time')
#
# def plot_gauge():
#     # https://plotly.com/python/gauge-charts/
#     # https://plotly.com/python/indicator/
#     fig = go.Figure()
#
#     fig.add_trace(go.Indicator(
#         value=200,
#         delta={'reference': 160},
#         gauge={
#             'axis': {'visible': False}},
#         domain={'row': 0, 'column': 0}))
#
#     fig.add_trace(go.Indicator(
#         value=120,
#         gauge={
#             'shape': "bullet",
#             'axis': {'visible': False}},
#         domain={'x': [0.05, 0.5], 'y': [0.15, 0.35]}))
#
#     fig.add_trace(go.Indicator(
#         mode="number+delta",
#         value=300,
#         domain={'row': 0, 'column': 1}))
#
#     fig.add_trace(go.Indicator(
#         mode="delta",
#         value=40,
#         domain={'row': 1, 'column': 1}))
#
#     fig.update_layout(
#         grid={'rows': 2, 'columns': 2, 'pattern': "independent"},
#         template={'data': {'indicator': [{
#             'title': {'text': "Speed"},
#             'mode': "number+delta+gauge",
#             'delta': {'reference': 90}}]
#         }})
#
#     fig.show()
#
# def example_scatter():
#     df = px.data.tips()
#     fig = px.scatter(df, x="total_bill", y="tip", facet_col="sex",
#                      width=800, height=400)
#
#     fig.update_layout(margin=dict(l=20, r=20, t=20, b=20),
#                       paper_bgcolor="LightSteelBlue")
#
#     fig.show()
#
# def main():
#     plot_gauge()
#     # example_scatter()
#     # sliders_buttons()
#
#
# if __name__ == '__main__':
#     main()
