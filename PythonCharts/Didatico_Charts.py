import numpy as np
import pandas as pd
import plot_extra as pe

import matplotlib.pyplot as plt
plt.rcParams.update(plt.rcParamsDefault)
#plt.rcParams['mathtext.fontset'] = 'cm'  # 'cm' Computer modern # 'dejavuserif', 'dejavusans'
#plt.rcParams['font.family'] = 'serif'
plt.rc('axes', unicode_minus=False)
plt.rcParams['text.usetex'] = 'True'
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath} \usepackage{crimson} \usepackage{siunitx}'


def plot_charts(figure_type='', caso=1):
    print("#####################")
    print("Function name: ", plot_charts.__name__)

    #######################
    print("---------------------")
    print("Opening CSV files: ")

    if caso == 1:
        filename = '..\Modelos\Didatico\RawData_Case1.csv'
        figfilename = '..\Modelos\Didatico\Case1'
    elif caso == 2:
        filename = '..\Modelos\Didatico\RawData_Case2.csv'
        figfilename = '..\Modelos\Didatico\Case2'
    else:
        filename = '..\Modelos\Didatico\RawData_Case3.csv'
        figfilename = '..\Modelos\Didatico\Case3'

    df = pd.read_csv(filepath_or_buffer=filename)
    print("    dataframe from:", filename)

    ###############################################################
    # size of the figure (in inches), and linestyles
    ###############################################################
    if figure_type == '.png':
        figsizex = 3.75
        figsizey = 7
    else:
        figsizex = 4
        figsizey = 5


    fig, axes = plt.subplots(4, 1, sharex=True,
                             figsize=(figsizex, figsizey),
                             num='Charts')

    axes[0].plot(df['time'],
                 df['Pload'],
                 color='black',
                 linewidth=1,
                 linestyle='solid',
                 label=r'Load')

    axes[1].plot(df['time'],
                 df['F'],
                 color='black',
                 linewidth=1,
                 linestyle='solid',
                 label=r'Frequency')

    axes[2].plot(df['time'],
                 df['Pgov'],
                 color='black',
                 linewidth=1,
                 linestyle='solid',
                 label=r'Gas Turbines')

    axes[3].plot(df['time'],
                 df['Pwf'],
                 color='black',
                 linewidth=1,
                 linestyle='solid',
                 label=r'Wind Farm')

    axes[3].plot(df['time'],
                 df['Pbat'],
                 color='red',
                 linewidth=1,
                 linestyle='solid',
                 label=r'Batteries')

    axes[3].plot(df['time'],
                 df['Pfc'],
                 color='blue',
                 linewidth=1,
                 linestyle='solid',
                 label=r'Fuel Cell')

    ##########################################################################
    # axis limits
    ##########################################################################
    axes[3].set_xticks(np.arange(0, 200, 10))
    axes[3].set_xlim([0, 120])

    ##########################################################################
    # axis names and legends
    ##########################################################################
    axes[3].set_xlabel(r'Time (\si{\second})')

    axes[0].set_ylabel(r'Load (\si{\mega \watt})')
    axes[1].set_ylabel(r'Frequency (\si{\hertz})')
    axes[2].set_ylabel(r'Generator (\si{\mega \watt})')
    axes[3].set_ylabel(r'Power (\si{\mega \watt})')

    axes[0].legend(loc='best', frameon=False, prop={'size': 9})
    axes[1].legend(loc='best', frameon=False, prop={'size': 9})
    axes[2].legend(loc='best', frameon=False, prop={'size': 9})
    axes[3].legend(loc='best', frameon=False, prop={'size': 9})

    ##########################################################################
    # align, tighten, shown and save
    ##########################################################################
    fig.align_ylabels(axes[:])
    fig.tight_layout()
    # fig.show()

    if figure_type == '.pdf':
        plt.savefig(figfilename + figure_type, format="pdf", bbox_inches="tight")
    elif figure_type == '.eps':
        plt.savefig(figfilename + figure_type, format='eps')
    elif figure_type == '.png':
        plt.savefig(figfilename + figure_type, format='png')

    plt.show()


def main():
    print("#####################")
    print("Function name: ", main.__name__)

    # figure_type = '.png'
    # figure_type = '.eps'
    figure_type = '.pdf'

    plot_charts(figure_type=figure_type, caso=1)

if __name__ == '__main__':
    main()

