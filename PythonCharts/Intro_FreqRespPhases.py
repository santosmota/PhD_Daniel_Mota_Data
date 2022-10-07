from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

import numpy as np
import pandas as pd
import scipy.io as sio
import plot_extra as pe

import matplotlib.pyplot as plt
plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams['mathtext.fontset'] = 'cm'  # 'cm' Computer modern # 'dejavuserif', 'dejavusans'
plt.rcParams['font.family'] = 'serif'
# plt.rcParams['font.serif'] = 'cmr10'  # 'https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/font_file.html
plt.rc('axes', unicode_minus=False)
#https://stackoverflow.com/questions/29188757/matplotlib-specify-format-of-floats-for-tick-labels

#https://matplotlib.org/stable/tutorials/text/usetex.html
# Matplotlib's LaTeX support requires a working LaTeX installation
# Text handling through LaTeX is slower than Matplotlib's very capable mathtext,
#  but is more flexible, since different LaTeX packages (font packages, math packages, etc.) can be used.
plt.rcParams['text.usetex'] = 'True'

#############
# solves a warning with a previous syntax
#https://stackoverflow.com/questions/65645194/warning-set-it-to-a-single-string-instead
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath} \usepackage{crimson} \usepackage{siunitx}'
# from matplotlib.ticker import FormatStrFormatter
# from matplotlib.offsetbox import AnchoredText

def plot_charts(figure_type='.pdf'):
    print("#####################")
    print("Function name: ", plot_charts.__name__)

    ###############################################################
    # CASES - file names - chart limits
    ###############################################################
    csv_full_path = '../Modelos/Intro/SimpleMass_RawData.csv'
    figure_full_path = '../Modelos/Intro/PhaseFreqControl' + figure_type

    ###############################################################
    # Opening csv file
    ###############################################################
    print('###########################')
    print('  CSV ')
    print('Chosen file: ', csv_full_path)

    # https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
    csv_df = pd.read_csv(csv_full_path, header=0)

    ###############################################################
    # size of the figure (in inches), and linestyles
    ###############################################################
    figsizex = 5
    figsizey = 5
    fig, axes = plt.subplots(3, 1, sharex=True,
                             figsize=(figsizex, figsizey),
                             num='Charts')

    axes[0].plot(csv_df['time'],
                 csv_df['pload'],
                 color='black',
                 linewidth=1,
                 linestyle='dashed',
                 label=r'Load')

    axes[0].plot(csv_df['time'],
                 csv_df['pmec'],
                 color=pe.cor_dalt['gray'],
                 linewidth=1,
                 linestyle='solid',
                 label=r'Generation')

    axes[1].plot(csv_df['time'],
                 csv_df['f'],
                 color='black',
                 linewidth=1,
                 linestyle='solid',
                 label=r'Frequency')

    axes[2].plot(csv_df['time'],
                 csv_df['pinert'],
                 color=pe.cor_dalt['red'],
                 linewidth=1,
                 linestyle='solid',
                 label=r'Inertial')

    axes[2].plot(csv_df['time'],
                 csv_df['pprim'],
                 color=pe.cor_dalt['blue'],
                 linewidth=1,
                 linestyle='solid',
                 label=r'Primary')

    axes[2].plot(csv_df['time'],
                 csv_df['psec'],
                 color=pe.cor_dalt['green'],
                 linewidth=1,
                 linestyle='solid',
                 label=r'Secondary')

    ##########################################################################
    # axis limits
    ##########################################################################
    axes[2].set_xticks(np.arange(0, 100, 20))
    axes[2].set_xlim([0, 80])

    axes[0].set_yticks(np.arange(0.50, 0.60, 0.02))
    axes[0].set_ylim([0.499, 0.56])

    axes[1].set_yticks(np.arange(0.98, 1.01, 0.005))
    axes[1].set_ylim([0.9875, 1.0005])

    axes[2].set_yticks(np.arange(0, 0.08, 0.02))
    axes[2].set_ylim([-0.01, 0.06])

    ##########################################################################
    # axis names
    ##########################################################################
    axes[2].set_xlabel(r'Time (\si{\milli \second})')

    axes[0].set_ylabel(r'Total power (\si{pu})')
    axes[1].set_ylabel(r'Frequency (\si{pu})')
    axes[2].set_ylabel(r'Reserve power (\si{pu})')

    ##########################################################################
    # chart identification - legend - abcdefghi
    ##########################################################################
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    # colors lightgray gray aliceblue whitesmoke
    # corlegenda = 'whitesmoke'
    #
    # axes[0][0].annotate(r'a', xy=(0.9, 0.15), xycoords='axes fraction',
    #                          bbox=dict(boxstyle='circle', fc=corlegenda))



    ##########################################################################
    # axis legends
    ##########################################################################
    axes[0].legend(loc='best', frameon=False, prop={'size': 10})
    axes[1].legend(loc='best', frameon=False, prop={'size': 10})
    axes[2].legend(loc='center right', frameon=False, prop={'size': 10})

    ##########################################################################
    # align, tighten, shown and save
    ##########################################################################
    fig.align_ylabels(axes[:])
    fig.tight_layout()
    # fig.show()

    if figure_type == '.pdf':
        plt.savefig(figure_full_path, format="pdf", bbox_inches="tight")
    elif figure_type == '.eps':
        plt.savefig(figure_full_path, format='eps')

    plt.show()


def main():
    print("#####################")
    print("Function name: ", main.__name__)

    figure_type = '.pdf'
    #figure_type = ''

    plot_charts(figure_type=figure_type)


if __name__ == '__main__':
    main()
