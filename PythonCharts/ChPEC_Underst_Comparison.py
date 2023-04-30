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
    csv_notch_full_path = '../Modelos/ChPEC/UnderstExp/Comp_viabcpqui_Neg_notch.csv'
    csv_DDRRF_full_path = '../Modelos/ChPEC/UnderstExp/Comp_viabcpqui_Neg_DDRRF.csv'

    figure_full_path = '../Modelos/ChPEC/PEC_CompRegulator_NotchDDRRF' + figure_type

    # time,vga,vgb,vgc,vca,vcb,vcc,ia,ib,ic,p,q,v,i

    df_notch = pd.read_csv(csv_notch_full_path)
    df_DDRRF = pd.read_csv(csv_DDRRF_full_path)

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
    line_style = 'solid'

    label_a = r'$a$'
    label_b = r'$b$'
    label_c = r'$c$'
    label_p = r'$p$'

    cor_a = pe.cor_dalt['red']
    cor_b = pe.cor_dalt['green']
    cor_c = pe.cor_dalt['blue']

    cor_p = 'black'

    ###############################################################
    # GRID VOLTAGE - NOTCH
    ###############################################################
    axes[0, 0].plot(df_notch['time'] * time_scaling,
                    df_notch['vga'],
                    color=cor_a,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_a)

    axes[0, 0].plot(df_notch['time'] * time_scaling,
                    df_notch['vgb'],
                    color=cor_b,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_b)

    axes[0, 0].plot(df_notch['time'] * time_scaling,
                    df_notch['vgc'],
                    color=cor_c,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_c)

    ###############################################################
    # GRID VOLTAGE - DDRRF
    ###############################################################
    axes[0, 1].plot(df_DDRRF['time'] * time_scaling,
                    df_DDRRF['vga'],
                    color=cor_a,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_a)

    axes[0, 1].plot(df_DDRRF['time'] * time_scaling,
                    df_DDRRF['vgb'],
                    color=cor_b,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_b)

    axes[0, 1].plot(df_DDRRF['time'] * time_scaling,
                    df_DDRRF['vgc'],
                    color=cor_c,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_c)

    ###############################################################
    # CONVERTER VOLTAGE - NOTCH
    ###############################################################
    axes[1, 0].plot(df_notch['time'] * time_scaling,
                    df_notch['vca'],
                    color=cor_a,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_a)

    axes[1, 0].plot(df_notch['time'] * time_scaling,
                    df_notch['vcb'],
                    color=cor_b,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_b)

    axes[1, 0].plot(df_notch['time'] * time_scaling,
                    df_notch['vcc'],
                    color=cor_c,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_c)

    ###############################################################
    # GRID VOLTAGE - DDRRF
    ###############################################################
    axes[1, 1].plot(df_DDRRF['time'] * time_scaling,
                    df_DDRRF['vca'],
                    color=cor_a,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_a)

    axes[1, 1].plot(df_DDRRF['time'] * time_scaling,
                    df_DDRRF['vcb'],
                    color=cor_b,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_b)

    axes[1, 1].plot(df_DDRRF['time'] * time_scaling,
                    df_DDRRF['vcc'],
                    color=cor_c,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_c)

    ###############################################################
    # GRID CURRENT - NOTCH
    ###############################################################
    axes[2, 0].plot(df_notch['time'] * time_scaling,
                    df_notch['ia'],
                    color=cor_a,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_a)

    axes[2, 0].plot(df_notch['time'] * time_scaling,
                    df_notch['ib'],
                    color=cor_b,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_b)

    axes[2, 0].plot(df_notch['time'] * time_scaling,
                    df_notch['ic'],
                    color=cor_c,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_c)

    ###############################################################
    # GRID CURRENT - DDRRF
    ###############################################################
    axes[2, 1].plot(df_DDRRF['time'] * time_scaling,
                    df_DDRRF['ia'],
                    color=cor_a,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_a)

    axes[2, 1].plot(df_DDRRF['time'] * time_scaling,
                    df_DDRRF['ib'],
                    color=cor_b,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_b)

    axes[2, 1].plot(df_DDRRF['time'] * time_scaling,
                    df_DDRRF['ic'],
                    color=cor_c,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_c)

    ###############################################################
    # POWER - NOTCH
    ###############################################################
    axes[3, 0].plot(df_notch['time'] * time_scaling,
                    df_notch['p'],
                    color=cor_p,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_p)

    ###############################################################
    # POWER - DDRRF
    ###############################################################
    axes[3, 1].plot(df_DDRRF['time'] * time_scaling,
                    df_DDRRF['p'],
                    color=cor_p,
                    linewidth=line_width,
                    linestyle=line_style,
                    label=label_p)


    ##########################################################################
    # axis limits
    ##########################################################################
    axes[0, 0].set_xticks(np.arange(0, 1000, 25))
    axes[0, 0].set_xlim([484, 600])

    axes[0, 0].set_yticks(np.arange(-2.0, 2.0, 1.0))
    axes[0, 0].set_ylim([-1.3, 1.3])

    axes[0, 1].set_yticks(np.arange(-2.0, 2.0, 1.0))
    axes[0, 1].set_ylim([-1.3, 1.3])

    axes[1, 0].set_yticks(np.arange(-2.0, 2.0, 1.0))
    axes[1, 0].set_ylim([-1.3, 1.3])

    axes[1, 1].set_yticks(np.arange(-2.0, 2.0, 1.0))
    axes[1, 1].set_ylim([-1.3, 1.3])

    axes[2, 0].set_yticks(np.arange(-0.25, 0.25, 0.05))
    axes[2, 0].set_ylim([-0.07, 0.1])

    axes[2, 1].set_yticks(np.arange(-0.25, 0.25, 0.05))
    axes[2, 1].set_ylim([-0.07, 0.1])

    axes[3, 0].set_yticks(np.arange(-0.3, 0.3, 0.05))
    axes[3, 0].set_ylim([-0.075, 0.075])

    axes[3, 1].set_yticks(np.arange(-0.3, 0.3, 0.05))
    axes[3, 1].set_ylim([-0.075, 0.075])

    ##########################################################################
    # axis names
    ##########################################################################
    axes[0, 0].title.set_text(r'Notch-based dual controller')
    axes[0, 1].title.set_text(r'DDRRF-based dual controller')


    axes[3, 0].set_xlabel(r'Time (\si{\milli\second})')  # , multialignment='center', ha='center')
    axes[3, 1].set_xlabel(r'Time (\si{\milli\second})')

    axes[0, 0].set_ylabel(r'Grid voltage (\si{pu})')
    axes[0, 1].set_ylabel(r'Grid voltage (\si{pu})')

    axes[1, 0].set_ylabel(r'Converter voltage (\si{pu})')
    axes[1, 1].set_ylabel(r'Converter voltage (\si{pu})')

    axes[2, 0].set_ylabel(r'Current (\si{pu})')
    axes[2, 1].set_ylabel(r'Current (\si{pu})')

    axes[3, 0].set_ylabel(r'Active Power (\si{pu})')
    axes[3, 1].set_ylabel(r'Active Power (\si{pu})')

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
