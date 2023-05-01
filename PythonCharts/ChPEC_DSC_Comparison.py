#################################################################
# Generates the comparison between notch, DSC (unbalanced grid voltage)
#   of the COMPEL
#################################################################

TO BE DONE!!!!!

import numpy as np
import pandas as pd
import plot_extra as pe

import matplotlib.pyplot as plt
plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams['mathtext.fontset'] = 'cm'  # 'cm' Computer modern # 'dejavuserif', 'dejavusans'
plt.rcParams['font.family'] = 'serif'
plt.rc('axes', unicode_minus=False)
plt.rcParams['text.usetex'] = 'True'

#############
# solves a warning with a previous syntax
#https://stackoverflow.com/questions/65645194/warning-set-it-to-a-single-string-instead
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath} \usepackage{crimson} \usepackage{siunitx}'
# from matplotlib.ticker import FormatStrFormatter
# from matplotlib.offsetbox import AnchoredText


def plot_chart(figure_type='.pdf'):
    print("#####################")
    print("Function name: ", plot_chart.__name__)

    ###############################################################
    # CASES - file names - chart limits
    ###############################################################
    csv_notch_full_path = '../Modelos/ChPEC/UnderstExp/Comp_viabcpqui_Neg_notch.csv'
    csv_DDRRF_full_path = '../Modelos/ChPEC/UnderstExp/Comp_viabcpqui_Neg_DDRRF.csv'

    figure_full_path = '../Modelos/ChPEC/PEC_CompRegulator_NotchDDRRF' + figure_type