#################################################################
# Generates the first comparison between notch, DDRRF, AMA
#   of the CPE-POWER ENG, Understanding Exp. Decaying paper
#################################################################

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
    csv_v_plus_full_path = '../Modelos/ChPEC/UnderstExp/BenchVoltPos.csv'
    csv_i_plus_full_path = '../Modelos/ChPEC/UnderstExp/BenchCurrPos.csv'

    csv_v_minus_full_path = '../Modelos/ChPEC/UnderstExp/BenchVoltNeg.csv'
    csv_i_minus_full_path = '../Modelos/ChPEC/UnderstExp/BenchCurrNeg.csv'

    figure_full_path = '../Modelos/ChPEC/PEC_NotchDDRRF' + figure_type

    # time,v_d_ideal,v_q_ideal,v_d_notch,v_q_notch,v_d_ddrrf,v_q_ddrrf,v_d_ama,v_q_ama

    df_v_plus = pd.read_csv(csv_v_plus_full_path)
    df_i_plus = pd.read_csv(csv_i_plus_full_path)

    df_v_minus = pd.read_csv(csv_v_minus_full_path)
    df_i_minus = pd.read_csv(csv_i_minus_full_path)

    time_scaling = 1000.0

    ###############################################################
    # size of the figure (in inches), and linestyles
    ###############################################################
    figsizex = 6
    figsizey = 6
    fig, axes = plt.subplots(4, 2, sharex=True,
                             figsize=(figsizex, figsizey),
                             num='Charts')

    line_width = 0.75
    line_style_ideal = ':'
    line_width_ideal = 1.0
    line_style = 'solid'

    label_ideal = r'Ideal'
    label_notch = r'Notch'
    label_DDRRF = r'DDRRF'
    label_AMA = r'AMA'

    cor_ideal = 'black'  # pe.cor_dalt['gray']
    cor_notch = pe.cor_dalt['red']
    cor_DDRRF = pe.cor_dalt['blue']

    ###############################################################
    # POSITIVE - DIRECT VOLTAGE
    ###############################################################
    axes[0, 0].plot(df_v_plus['time'] * time_scaling,
                    df_v_plus['v_d_notch'],
                    color=cor_notch,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_notch)

    axes[0, 0].plot(df_v_plus['time'] * time_scaling,
                    df_v_plus['v_d_ddrrf'],
                    color=cor_DDRRF,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_DDRRF)

    axes[0, 0].plot(df_v_plus['time'] * time_scaling,
                    df_v_plus['v_d_ideal'],
                    color=cor_ideal,
                    linewidth=line_width_ideal,
                    linestyle=line_style_ideal,
                    label=label_ideal)

    ###############################################################
    # POSITIVE - DIRECT CURRENT
    ###############################################################
    axes[0, 1].plot(df_i_plus['time'] * time_scaling,
                    df_i_plus['i_d_notch'],
                    color=cor_notch,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_notch)

    axes[0, 1].plot(df_i_plus['time'] * time_scaling,
                    df_i_plus['i_d_ddrrf'],
                    color=cor_DDRRF,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_DDRRF)

    axes[0, 1].plot(df_i_plus['time'] * time_scaling,
                    df_i_plus['i_d_ideal'],
                    color=cor_ideal,
                    linewidth=line_width_ideal,
                    linestyle=line_style_ideal,
                    label=label_ideal)

    ###############################################################
    # POSITIVE - QUADRATURE VOLTAGE
    ###############################################################
    axes[1, 0].plot(df_v_plus['time'] * time_scaling,
                    df_v_plus['v_q_notch'],
                    color=cor_notch,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_notch)

    axes[1, 0].plot(df_v_plus['time'] * time_scaling,
                    df_v_plus['v_q_ddrrf'],
                    color=cor_DDRRF,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_DDRRF)

    axes[1, 0].plot(df_v_plus['time'] * time_scaling,
                    df_v_plus['v_q_ideal'],
                    color=cor_ideal,
                    linewidth=line_width_ideal,
                    linestyle=line_style_ideal,
                    label=label_ideal)

    ###############################################################
    # POSITIVE - QUADRATURE CURRENT
    ###############################################################
    axes[1, 1].plot(df_i_plus['time'] * time_scaling,
                    df_i_plus['i_q_notch'],
                    color=cor_notch,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_notch)

    axes[1, 1].plot(df_i_plus['time'] * time_scaling,
                    df_i_plus['i_q_ddrrf'],
                    color=cor_DDRRF,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_DDRRF)

    axes[1, 1].plot(df_i_plus['time'] * time_scaling,
                    df_i_plus['i_q_ideal'],
                    color=cor_ideal,
                    linewidth=line_width_ideal,
                    linestyle=line_style_ideal,
                    label=label_ideal)

    ###############################################################
    # NEGATIVE - DIRECT VOLTAGE
    ###############################################################
    axes[2, 0].plot(df_v_minus['time'] * time_scaling,
                    df_v_minus['v_d_notch'],
                    color=cor_notch,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_notch)

    axes[2, 0].plot(df_v_minus['time'] * time_scaling,
                    df_v_minus['v_d_ddrrf'],
                    color=cor_DDRRF,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_DDRRF)

    axes[2, 0].plot(df_v_minus['time'] * time_scaling,
                    df_v_minus['v_d_ideal'],
                    color=cor_ideal,
                    linewidth=line_width_ideal,
                    linestyle=line_style_ideal,
                    label=label_ideal)

    ###############################################################
    # NEGATIVE - DIRECT CURRENT
    ###############################################################
    axes[2, 1].plot(df_i_minus['time'] * time_scaling,
                    df_i_minus['i_d_notch'],
                    color=cor_notch,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_notch)

    axes[2, 1].plot(df_i_minus['time'] * time_scaling,
                    df_i_minus['i_d_ddrrf'],
                    color=cor_DDRRF,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_DDRRF)

    axes[2, 1].plot(df_i_minus['time'] * time_scaling,
                    df_i_minus['i_d_ideal'],
                    color=cor_ideal,
                    linewidth=line_width_ideal,
                    linestyle=line_style_ideal,
                    label=label_ideal)

    ###############################################################
    # NEGATIVE - QUADRATURE VOLTAGE
    ###############################################################
    axes[3, 0].plot(df_v_minus['time'] * time_scaling,
                    df_v_plus['v_q_notch'],
                    color=cor_notch,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_notch)

    axes[3, 0].plot(df_v_minus['time'] * time_scaling,
                    df_v_minus['v_q_ddrrf'],
                    color=cor_DDRRF,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_DDRRF)

    axes[3, 0].plot(df_v_minus['time'] * time_scaling,
                    df_v_minus['v_q_ideal'],
                    color=cor_ideal,
                    linewidth=line_width_ideal,
                    linestyle=line_style_ideal,
                    label=label_ideal)

    ###############################################################
    # NEGATIVE - QUADRATURE CURRENT
    ###############################################################
    axes[3, 1].plot(df_i_minus['time'] * time_scaling,
                    df_i_minus['i_q_notch'],
                    color=cor_notch,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_notch)

    axes[3, 1].plot(df_i_minus['time'] * time_scaling,
                    df_i_minus['i_q_ddrrf'],
                    color=cor_DDRRF,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_DDRRF)

    axes[3, 1].plot(df_i_minus['time'] * time_scaling,
                    df_i_minus['i_q_ideal'],
                    color=cor_ideal,
                    linewidth=line_width_ideal,
                    linestyle=line_style_ideal,
                    label=label_ideal)

    ##########################################################################
    # axis limits
    ##########################################################################
    axes[0, 0].set_xticks(np.arange(0, 100, 5))
    axes[0, 0].set_xlim([0, 35])

    # axes[0, 0].set_yticks(np.arange(0.50, 0.60, 0.01))
    # axes[0, 0].set_ylim([0.499, 0.56])

    ##########################################################################
    # axis names
    ##########################################################################
    axes[3, 0].set_xlabel(r'Time (\si{\milli\second})')
    axes[3, 1].set_xlabel(r'Time (\si{\milli\second})')

    axes[0, 0].set_ylabel(r'Voltage $d+$ (\si{pu})')
    axes[0, 1].set_ylabel(r'Current $d+$ (\si{pu})')

    axes[1, 0].set_ylabel(r'Voltage $q+$ (\si{pu})')
    axes[1, 1].set_ylabel(r'Current $q+$ (\si{pu})')

    axes[2, 0].set_ylabel(r'Voltage $d-$ (\si{pu})')
    axes[2, 1].set_ylabel(r'Current $d-$ (\si{pu})')

    axes[3, 0].set_ylabel(r'Voltage $q-$ (\si{pu})')
    axes[3, 1].set_ylabel(r'Current $q-$ (\si{pu})')

    ##########################################################################
    # chart identification - legend - abcdefghi
    ##########################################################################
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    # colors lightgray gray aliceblue whitesmoke
    corlegenda = 'whitesmoke'
    #
    axes[0, 0].annotate(r'a', xy=(0.92, 0.15), xycoords='axes fraction',
                        bbox=dict(boxstyle='circle', fc=corlegenda))

    axes[0, 1].annotate(r'b', xy=(0.92, 0.83), xycoords='axes fraction',
                        bbox=dict(boxstyle='circle', fc=corlegenda))

    axes[1, 0].annotate(r'c', xy=(0.92, 0.83), xycoords='axes fraction',
                        bbox=dict(boxstyle='circle', fc=corlegenda))

    axes[1, 1].annotate(r'd', xy=(0.92, 0.83), xycoords='axes fraction',
                        bbox=dict(boxstyle='circle', fc=corlegenda))

    axes[2, 0].annotate(r'e', xy=(0.92, 0.83), xycoords='axes fraction',
                        bbox=dict(boxstyle='circle', fc=corlegenda))

    axes[2, 1].annotate(r'f', xy=(0.92, 0.83), xycoords='axes fraction',
                        bbox=dict(boxstyle='circle', fc=corlegenda))

    axes[3, 0].annotate(r'g', xy=(0.92, 0.83), xycoords='axes fraction',
                        bbox=dict(boxstyle='circle', fc=corlegenda))

    axes[3, 1].annotate(r'h', xy=(0.92, 0.83), xycoords='axes fraction',
                        bbox=dict(boxstyle='circle', fc=corlegenda))

    ##########################################################################
    # axis legends
    ##########################################################################
    axes[0, 0].legend(loc='best', frameon=False, prop={'size': 10})

    ##########################################################################
    # align, tighten, shown and save
    ##########################################################################
    fig.align_ylabels(axes[:])
    fig.tight_layout()

    if figure_type == '.pdf':
        plt.savefig(figure_full_path, format="pdf", bbox_inches="tight")
    elif figure_type == '.eps':
        plt.savefig(figure_full_path, format='eps')

    plt.show()


#####################################################
# main
#####################################################
def main():
    print("#####################")
    print("Function name: ", main.__name__)

    plot_chart()

if __name__ == '__main__':
    main()
