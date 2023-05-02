#################################################################
# Generates the comparison between notch, DSC (unbalanced grid voltage)
#   of the COMPEL
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
    csv_notch_full_path = '../Modelos/ChPEC/DSC/Application_Unb_Notch.txt'
    csv_dscab_full_path = '../Modelos/ChPEC/DSC/Application_Unb_DSCab.txt'
    csv_dscdq_full_path = '../Modelos/ChPEC/DSC/Application_Unb_DSCdq.txt'

    figure_full_path = '../Modelos/ChPEC/PEC_CompRegulator_NotchDSC' + figure_type

    colunas = ['time', 'vga', 'vgb', 'vgc', 'ia', 'ib', 'ic', 'f', 'p', 'q', 'vdc', 'n']

    df_notch = pd.read_csv(csv_notch_full_path, names=colunas, header=None)
    df_dscab = pd.read_csv(csv_dscab_full_path, names=colunas, header=None)
    df_dscdq = pd.read_csv(csv_dscdq_full_path, names=colunas, header=None)

    time_scaling = 1000.0

    ###############################################################
    # size of the figure (in inches), and linestyles
    ###############################################################
    figsizex = 6
    figsizey = 6
    fig, axes = plt.subplots(4, 2, # sharex=True,
                             figsize=(figsizex, figsizey),
                             num='Charts')

    line_width = 0.75
    line_style = 'solid'

    label_va = r'$v_a$'
    label_vb = r'$v_b$'
    label_vc = r'$v_c$'

    cor_va = pe.cor_dalt['pink']
    cor_vb = pe.cor_dalt['green']
    cor_vc = pe.cor_dalt['blue']

    cor_notch = pe.cor_dalt['red']
    cor_dscab = 'black'
    cor_dscdq = 'black'

    label_notch = r'Notch'
    label_dscab = r'DSC$_{\alpha \beta}$'
    label_dscdq = r'DSC$_{dq}$'

    line_style_notch = 'solid'
    line_style_dscab = '-.'
    line_style_dscdq = ':'

    for col in range(0, 2):
        ###############################################################
        # GRID VOLTAGE
        ###############################################################
        axes[0, col].plot(df_notch['time'] * time_scaling,
                          df_notch['vga'],
                          color=cor_va,
                          linewidth=line_width,
                          linestyle=line_style,
                          label=label_va)

        axes[0, col].plot(df_notch['time'] * time_scaling,
                          df_notch['vgb'],
                          color=cor_vb,
                          linewidth=line_width,
                          linestyle=line_style,
                          label=label_vb)

        axes[0, col].plot(df_notch['time'] * time_scaling,
                          df_notch['vgc'],
                          color=cor_vc,
                          linewidth=line_width,
                          linestyle=line_style,
                          label=label_vc)

        ###############################################################
        # Active Power
        ###############################################################
        axes[1, col].plot(df_notch['time'] * time_scaling,
                          df_notch['p'],
                          color=cor_notch,
                          linewidth=line_width,
                          linestyle=line_style_notch,
                          label=label_notch)

        axes[1, col].plot(df_dscab['time'] * time_scaling,
                          df_dscab['p'],
                          color=cor_dscab,
                          linewidth=line_width,
                          linestyle=line_style_dscab,
                          label=label_dscab)

        axes[1, col].plot(df_dscab['time'] * time_scaling,
                          df_dscab['p'],
                          color=cor_dscdq,
                          linewidth=line_width,
                          linestyle=line_style_dscdq,
                          label=label_dscdq)

        ###############################################################
        # Reactive Power
        ###############################################################
        axes[2, col].plot(df_notch['time'] * time_scaling,
                          df_notch['q'],
                          color=cor_notch,
                          linewidth=line_width,
                          linestyle=line_style_notch,
                          label=label_notch)

        axes[2, col].plot(df_dscab['time'] * time_scaling,
                          df_dscab['q'],
                          color=cor_dscab,
                          linewidth=line_width,
                          linestyle=line_style_dscab,
                          label=label_dscab)

        axes[2, col].plot(df_dscab['time'] * time_scaling,
                          df_dscab['q'],
                          color=cor_dscdq,
                          linewidth=line_width,
                          linestyle=line_style_dscdq,
                          label=label_dscdq)

        ###############################################################
        # DC voltage
        ###############################################################
        axes[3, col].plot(df_notch['time'] * time_scaling,
                          df_notch['vdc'],
                          color=cor_notch,
                          linewidth=line_width,
                          linestyle=line_style_notch,
                          label=label_notch)

        axes[3, col].plot(df_dscab['time'] * time_scaling,
                          df_dscab['vdc'],
                          color=cor_dscab,
                          linewidth=line_width,
                          linestyle=line_style_dscab,
                          label=label_dscab)

        axes[3, col].plot(df_dscab['time'] * time_scaling,
                          df_dscab['vdc'],
                          color=cor_dscdq,
                          linewidth=line_width,
                          linestyle=line_style_dscdq,
                          label=label_dscdq)

    ##########################################################################
    # axis limits
    ##########################################################################
    for row in range(0, 4):
        axes[row, 0].set_xticks(np.arange(900, 2000, 100))
        axes[row, 0].set_xlim([900, 1400])

    for row in range(0, 4):
        axes[row, 1].set_xticks(np.arange(980, 1050, 20))
        axes[row, 1].set_xlim([980, 1040])

    for col in range(0, 2):
        axes[0, col].set_yticks(np.arange(-2.0, 2.0, 1.0))
        axes[0, col].set_ylim([-1.2, 1.2])

        axes[1, col].set_yticks(np.arange(-0.01, 0.03, 0.01))
        axes[1, col].set_ylim([-0.01, 0.02])

        axes[2, col].set_yticks(np.arange(-0.005, 0.010, 0.005))
        axes[2, col].set_ylim([-0.005, 0.005])

        axes[3, col].set_yticks(np.arange(0.990, 1.010, 0.005))
        axes[3, col].set_ylim([0.990, 1.005])

    ##########################################################################
    # axis names
    ##########################################################################
    axes[0, 0].title.set_text(r'Complete transient')
    axes[0, 1].title.set_text(r'Detail')

    axes[3, 0].set_xlabel(r'Time (\si{\milli\second})')  # , multialignment='center', ha='center')
    axes[3, 1].set_xlabel(r'Time (\si{\milli\second})')

    axes[0, 0].set_ylabel(r'Grid voltage (\si{pu})')
    axes[0, 1].set_ylabel(r'Grid voltage (\si{pu})')

    axes[1, 0].set_ylabel(r'Active power (\si{pu})')
    axes[1, 1].set_ylabel(r'Active power (\si{pu})')

    axes[2, 0].set_ylabel(r'Reactive power (\si{pu})')
    axes[2, 1].set_ylabel(r'Reactive power (\si{pu})')

    axes[3, 0].set_ylabel(r'Dc voltage (\si{pu})')
    axes[3, 1].set_ylabel(r'Dc voltage (\si{pu})')

    ##########################################################################
    # chart identification - legend - abcdefghi
    ##########################################################################
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    # colors lightgray gray aliceblue whitesmoke
    corlegenda = 'whitesmoke'
    #
    axes[0, 0].annotate(r'a', xy=(0.92, 0.83), xycoords='axes fraction',
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
    axes[0, 0].legend(loc='lower right', frameon=True, prop={'size': 10})
    axes[1, 0].legend(loc='lower right', frameon=True, prop={'size': 10})

    ##########################################################################
    # align, tighten, shown and save
    ##########################################################################
    fig.align_ylabels(axes[:])
    # fig.align_xlabels(axes[:])
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


