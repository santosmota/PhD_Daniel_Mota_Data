#################################################################
# Generates 3 charts with varying frequency,
# DSC ceiling, floor, weighted
#   of the COMPEL - DSC paper
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

    Fn = 60.0
    Tn = 1.0 / Fn

    ###############################################################
    # CASES - file names - chart limits
    ###############################################################
    csv_full_path = '../Modelos/ChPEC/DSC/FreqAdaptive_Raw.txt'

    figure_full_path = '../Modelos/ChPEC/PEC_DSC_FrequencyAdaptive' + figure_type

    colunas = ['time', 'vd', 'vq', 'vdr', 'vqr', 'vdc', 'vqc', 'vdf', 'vqf', 'vdw', 'vqw', 'f', 'n', 'va', 'vb', 'vc']

    df = pd.read_csv(csv_full_path, names=colunas, header=None)

    ###############################################################
    # size of the figure (in inches), and linestyles
    ###############################################################
    figsizex = 5
    figsizey = 6
    fig, axes = plt.subplots(4, 1, sharex=True,
                             figsize=(figsizex, figsizey),
                             num='Charts')

    line_width = 0.75
    line_style = 'solid'

    ###############################################################
    # VOLTAGES ABC
    ###############################################################
    axes[0].plot(df['time'], df['va'],
                 color=pe.cor_dalt['red'],
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_a$')

    axes[0].plot(df['time'], df['vb'],
                 color=pe.cor_dalt['green'],
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_b$')

    axes[0].plot(df['time'], df['vc'],
                 color=pe.cor_dalt['blue'],
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_c$')

    ###############################################################
    # delayed samples
    ###############################################################
    axes[1].plot(df['time'].to_numpy(), np.ceil(df['n'].to_numpy()),
                 color=pe.cor_dalt['red'],
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$n_c$')

    axes[1].plot(df['time'], df['n'],
                 color=pe.cor_dalt['green'],
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$n$')

    axes[1].plot(df['time'].to_numpy(), np.floor(df['n'].to_numpy()),
                 color=pe.cor_dalt['blue'],
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$n_f$')

    ###############################################################
    # OUTPUTS - DIRECT
    ###############################################################
    axes[2].plot(df['time'], df['vdc'],
                 color=pe.cor_dalt['red'],
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_{d+c}$')

    axes[2].plot(df['time'], df['vdw'],
                 color=pe.cor_dalt['green'],
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_{d+w}$')

    axes[2].plot(df['time'], df['vdf'],
                 color=pe.cor_dalt['blue'],
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_{d+f}$')

    ###############################################################
    # OUTPUTS - DIRECT
    ###############################################################
    axes[3].plot(df['time'], df['vqc'],
                 color=pe.cor_dalt['red'],
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_{q+c}$')

    axes[3].plot(df['time'], df['vqw'],
                 color=pe.cor_dalt['green'],
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_{q+w}$')

    axes[3].plot(df['time'], df['vqf'],
                 color=pe.cor_dalt['blue'],
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_{q+f}$')

    ##########################################################################
    # axis limits
    ##########################################################################
    axes[0].set_xticks(np.arange(0, 0.5, 0.05))
    axes[0].set_xlim([0, 0.25])
    # axes[0].set_xticklabels(['$0T$', '$T/4$', '$T/2$', '$3T/4$', '$T$'])

    axes[2].set_yticks(np.arange(0.994, 1.006, 0.002))
    axes[2].set_ylim([0.997, 1.003])

    axes[3].set_yticks(np.arange(-0.004, 0.006, 0.002))
    axes[3].set_ylim([-0.003, 0.003])

    ##########################################################################
    # axis names
    ##########################################################################
    # axes[1].set_xlabel(r'Time (\si{\milli\second})')
    axes[2].set_xlabel(r'Time (s)')

    axes[0].set_ylabel(r'Voltages $abc$ frame (\si{pu})')
    axes[1].set_ylabel(r'Samples equiv. $T/4$')
    axes[2].set_ylabel(r'Voltages $d+$ axis (\si{pu})')
    axes[3].set_ylabel(r'Voltages $q+$ axis (\si{pu})')

    ##########################################################################
    # chart identification - legend - abcdefghi
    ##########################################################################
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    # colors lightgray gray aliceblue whitesmoke
    corlegenda = 'whitesmoke'
    #
    # axes[0].annotate(r'a', xy=(0.7, 0.82), xycoords='axes fraction',
    #                  bbox=dict(boxstyle='circle', fc=corlegenda))

    # axes[1].annotate(r'b', xy=(0.7, 0.82), xycoords='axes fraction',
    #                  bbox=dict(boxstyle='circle', fc=corlegenda))

    ##########################################################################
    # axis legends
    ##########################################################################
    axes[0].legend(loc='center right', frameon=True, prop={'size': 10})
    axes[1].legend(loc='lower right', frameon=True, prop={'size': 10})
    axes[2].legend(loc='lower right', frameon=True, prop={'size': 10})
    axes[3].legend(loc='lower right', frameon=True, prop={'size': 10})

    ##########################################################################
    # align, tighten, shown and save
    ##########################################################################
    fig.align_ylabels(axes[:])
    fig.tight_layout()

    if figure_type == '.pdf':
        fig.savefig(figure_full_path, format="pdf", bbox_inches="tight")
    elif figure_type == '.eps':
        fig.savefig(figure_full_path, format='eps')

    ##########################################################################
    # show plot
    ##########################################################################
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

