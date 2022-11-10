import pathlib
from dash import Dash, html, dcc, ctx
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output
import pandas as pd

import numpy as np
import pandas as pd
import plot_extra as pe

import matplotlib.pyplot as plt

#########################
# deployment
# https://www.youtube.com/watch?v=Gv910_b5ID0


##########################
# this does not seem to work
# load_figure_template('CYBORG')   # LUX DARKLY CYBORG
# https://towardsdatascience.com/3-easy-ways-to-make-your-dash-application-look-better-3e4cfefaf772

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("assets").resolve()

c = DATA_PATH.joinpath('Case2.png')
b = DATA_PATH.joinpath('Case2.png').as_posix()
a = str(DATA_PATH.joinpath('Case2.png').as_posix())

df1 = pd.read_csv(DATA_PATH.joinpath('RawData_Case1.csv'))
df2 = pd.read_csv(DATA_PATH.joinpath('RawData_Case2.csv'))
df3 = pd.read_csv(DATA_PATH.joinpath('RawData_Case3.csv'))



###############################################################
# size of the figure (in inches), and linestyles
###############################################################
figsizex = 3.75
figsizey = 7
fig, axes = plt.subplots(4, 1, sharex=True,
                         figsize=(figsizex, figsizey),
                         num='Charts')

axes[0].plot(df1['time'],
             df1['Pload'],
             color='black',
             linewidth=1,
             linestyle='solid',
             label=r'Load')

axes[0].plot(df2['time'],
             df2['Pload'],
             color='red',
             linewidth=1,
             linestyle='solid',
             label=r'Load')

fig.show()

a = 2