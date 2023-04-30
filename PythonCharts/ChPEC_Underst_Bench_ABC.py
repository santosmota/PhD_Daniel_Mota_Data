#################################################################
# Generates the ABC values that are the source for the
#   first comparison between notch, DDRRF, AMA
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
    csv_full_path = '../Modelos/ChPEC/UnderstExp/BenchABC.csv'

    figure_full_path = '../Modelos/ChPEC/PEC_NotchDDRRF_abc' + figure_type

    # time,vga,vgb,vgc,vca,vcb,vcc,ia,ib,ic,p,q,v,i

    df = pd.read_csv(csv_full_path)

    time_scaling = 1000.0

    ###############################################################
    # size of the figure (in inches), and linestyles
    ###############################################################
    figsizex = 5
    figsizey = 5
    fig, axes = plt.subplots(3, 1, sharex=True,
                             figsize=(figsizex, figsizey),
                             num='Charts')

    line_width = 0.75
    line_style = 'solid'

    cor_a = pe.cor_dalt['red']
    cor_b = pe.cor_dalt['green']
    cor_c = pe.cor_dalt['blue']

    cor_p = pe.cor_dalt['red']
    cor_q = pe.cor_dalt['blue']

    ###############################################################
    # VOLTAGE
    ###############################################################
    axes[0].plot(df['time'] * time_scaling,
                 df['vga'],
                 color=cor_a,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_a$')

    axes[0].plot(df['time'] * time_scaling,
                 df['vgb'],
                 color=cor_b,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_b$')

    axes[0].plot(df['time'] * time_scaling,
                 df['vgc'],
                 color=cor_c,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_c$')

    ###############################################################
    # CURRENT
    ###############################################################
    axes[1].plot(df['time'] * time_scaling,
                 df['ia'],
                 color=cor_a,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$i_a$')

    axes[1].plot(df['time'] * time_scaling,
                 df['ib'],
                 color=cor_b,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$i_b$')

    axes[1].plot(df['time'] * time_scaling,
                 df['ic'],
                 color=cor_c,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$i_c$')

    ###############################################################
    # POWERS
    ###############################################################
    axes[2].plot(df['time'] * time_scaling,
                 df['p'],
                 color=cor_p,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'Active')

    axes[2].plot(df['time'] * time_scaling,
                 df['q'],
                 color=cor_q,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'Reactive')

    ##########################################################################
    # axis limits
    ##########################################################################
    axes[0].set_xticks(np.arange(0, 300, 20))
    axes[0].set_xlim([0, 180])

    # axes[0, 0].set_yticks(np.arange(-2.0, 2.0, 0.5))
    # axes[0, 0].set_ylim([0.499, 0.56])

    ##########################################################################
    # axis names
    ##########################################################################
    axes[2].set_xlabel(r'Time (\si{\milli\second})')

    axes[0].set_ylabel(r'Voltage (\si{pu})')
    axes[1].set_ylabel(r'Current (\si{pu})')
    axes[2].set_ylabel(r'Power (\si{pu})')

    ##########################################################################
    # chart identification - legend - abcdefghi
    ##########################################################################
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    # colors lightgray gray aliceblue whitesmoke
    corlegenda = 'whitesmoke'
    #
    axes[0].annotate(r'a', xy=(0.9, 0.82), xycoords='axes fraction',
                     bbox=dict(boxstyle='circle', fc=corlegenda))

    axes[1].annotate(r'b', xy=(0.9, 0.82), xycoords='axes fraction',
                     bbox=dict(boxstyle='circle', fc=corlegenda))

    axes[2].annotate(r'c', xy=(0.9, 0.82), xycoords='axes fraction',
                     bbox=dict(boxstyle='circle', fc=corlegenda))

    ##########################################################################
    # axis legends
    ##########################################################################
    axes[0].legend(loc='lower right', frameon=True, prop={'size': 10})
    axes[1].legend(loc='lower right', frameon=True, prop={'size': 10})
    axes[2].legend(loc='lower right', frameon=True, prop={'size': 10})

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

