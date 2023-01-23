#################################################################
# Generates figure
# which contains the steps of 1.2MW with the Matlab model
#   rotating mass model + reserves with time delays (Low-pass filters)
#################################################################

import numpy as np
import pandas as pd
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

#####################################################
# plot eigen value charts and the frequency measurement from a set of csv files
#####################################################
def plot_fmeas_from_csvs(simcount_total=7,
                         csvfolder="../Modelos/PrimReserveSharing/",
                         timeoffset=0.0,
                         ):
    print("#####################")
    print("Function name: ", plot_fmeas_from_csvs.__name__)

    figstepsname = csvfolder + '/ChFreq_Steps_6MW_Matlab.pdf'

    ##########################################################################
    # figure
    ##########################################################################
    figsizex = 5
    figsizey = 6
    fig_steps, axs_steps = plt.subplots(4, 1, sharex=True,
                                        figsize=(figsizex, figsizey),
                                        num='Step')

    ##########################################################################
    # style of the plots
    ##########################################################################
    cores = []
    legendas = []
    legendas_freq = []
    marker = []
    estilos = []
    for simcount in range(0, simcount_total, 1):
        if simcount == 0:
            cores.append(pe.cor_dalt['red'])
            legendas.append('Generation. Primary: GTs only')
            legendas_freq.append('Primary: GTs only')
            marker.append('x')
            estilos.append('-')  # , ':', '-.']
        elif simcount == 1:
            cores.append(pe.cor_dalt['gray'])
            legendas.append('Generation. Primary: GTs+ESS')
            legendas_freq.append('Primary: GTs+ESS')
            marker.append('+')
            estilos.append(':')
        elif simcount == simcount_total - 1:
            cores.append(pe.cor_dalt['blue'])
            legendas.append('Generation. Primary: ESS only')
            legendas_freq.append('Primary: ESS only')
            marker.append('*')
            estilos.append('-.')
        else:
            cores.append(pe.cor_dalt['gray'])
            legendas.append('')
            legendas_freq.append('')
            marker.append('+')
            estilos.append(':')

    grossuras = 0.75
    markersize = 5

    ##########################################################################
    # plotting the eigen values
    ##########################################################################
    for simcount in range(0, simcount_total, 1):

        csvname = csvfolder + "/matstep_6MW_run_" + str(simcount+1) + '.csv'

        df_td = pd.read_csv(csvname,
                            names=['time', 'F', 'step', 'PfcrGT1', 'PfcrGT2', 'PfcrESS'],
                            header=None)

        if simcount == 0:
            axs_steps[0].plot(df_td['time'] + timeoffset,
                          df_td['step'] + 44.0,
                          linestyle='dashed',
                          linewidth=grossuras,
                          color='black',
                          label='Electric load (consumption)')

        axs_steps[0].plot(df_td['time'] + timeoffset,
                          df_td['PfcrGT1'] + df_td['PfcrGT2'] + df_td['PfcrESS'] + 44.0,
                          linestyle=estilos[simcount],
                          linewidth=grossuras,
                          color=cores[simcount],
                          label=legendas[simcount])

        axs_steps[1].plot(df_td['time'] + timeoffset,
                       df_td['F'],
                       linestyle=estilos[simcount],
                       linewidth=grossuras,
                       color=cores[simcount],
                       label=legendas_freq[simcount])

        axs_steps[2].plot(df_td['time'] + timeoffset,
                          df_td['PfcrGT1'] + df_td['PfcrGT2'] + 44.0,
                          linestyle=estilos[simcount],
                          linewidth=grossuras,
                          color=cores[simcount],
                          label=legendas[simcount])

        axs_steps[3].plot(df_td['time'] + timeoffset,
                          df_td['PfcrESS'],
                          linestyle=estilos[simcount],
                          linewidth=grossuras,
                          color=cores[simcount],
                          label=legendas[simcount])
    ##########################################################################
    # chart identification - legend - abcdefghi
    ##########################################################################
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    # colors lightgray gray aliceblue whitesmoke
    corlegenda = 'whitesmoke'
    #
    axs_steps[0].annotate(r'a', xy=(0.05, 0.75), xycoords='axes fraction',
                          bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[1].annotate(r'b', xy=(0.05, 0.75), xycoords='axes fraction',
                          bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[2].annotate(r'c', xy=(0.05, 0.75), xycoords='axes fraction',
                          bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[3].annotate(r'd', xy=(0.05, 0.75), xycoords='axes fraction',
                          bbox=dict(boxstyle='circle', fc=corlegenda))

    ##########################################################################
    # chart annotations
    ##########################################################################
    axs_steps[1].annotate(r'GTs:0MW/Hz ESS:12MW/Hz', xy=(6, 48.2), xycoords='data', color=pe.cor_dalt['blue'])
    axs_steps[1].annotate(r'GTs:2MW/Hz ESS:10MW/Hz', xy=(6, 48.7), xycoords='data', color=pe.cor_dalt['gray'])
    axs_steps[1].annotate(r'GTs:4MW/Hz ESS:8MW/Hz', xy=(6, 49.2), xycoords='data', color=pe.cor_dalt['gray'])

    axs_steps[1].annotate(r'Unstable',
                          xy=(8, 47.5), xycoords='data',
                          xytext=(8.75, 47.8), textcoords='data',
                          ha='left',
                          color=pe.cor_dalt['blue'],
                          arrowprops=dict(arrowstyle="->", connectionstyle="arc3",color=pe.cor_dalt['blue']))

    axs_steps[2].annotate(r'GTs:0MW/Hz ESS:12MW/Hz', xy=(3, 44), xycoords='data', color=pe.cor_dalt['blue'])
    axs_steps[2].annotate(r'GTs:2MW/Hz ESS:10MW/Hz', xy=(3, 45), xycoords='data', color=pe.cor_dalt['gray'])
    axs_steps[2].annotate(r'GTs:4MW/Hz ESS:8MW/Hz', xy=(3, 46), xycoords='data', color=pe.cor_dalt['gray'])
    axs_steps[2].annotate(r'GTs:6MW/Hz ESS:6MW/Hz', xy=(3, 47), xycoords='data', color=pe.cor_dalt['gray'])
    axs_steps[2].annotate(r'GTs:8MW/Hz ESS:4MW/Hz', xy=(4, 48), xycoords='data', color=pe.cor_dalt['gray'])
    axs_steps[2].annotate(r'GTs:10MW/Hz ESS:2MW/Hz', xy=(5, 49), xycoords='data', color=pe.cor_dalt['gray'])
    axs_steps[2].annotate(r'GTs:12MW/Hz ESS:0MW/Hz', xy=(6, 50), xycoords='data', color=pe.cor_dalt['red'])

    axs_steps[3].annotate(r'ESS:0MW/Hz GTs:12MW/Hz', xy=(5, 0), xycoords='data', color=pe.cor_dalt['red'])
    axs_steps[3].annotate(r'ESS:2MW/Hz GTs:10MW/Hz', xy=(5, 1), xycoords='data', color=pe.cor_dalt['gray'])
    axs_steps[3].annotate(r'ESS:4MW/Hz GTs:8MW/Hz', xy=(5, 2), xycoords='data', color=pe.cor_dalt['gray'])
    axs_steps[3].annotate(r'ESS:6MW/Hz GTs:6MW/Hz', xy=(2, 2.5), xycoords='data', color=pe.cor_dalt['gray'])
    axs_steps[3].annotate(r'ESS saturates for gains $\ge$ 6MW/Hz', xy=(1.5, 3.25), xycoords='data', color='black')

    ##########################################################################
    # axis names
    ##########################################################################
    axs_steps[3].set_xlabel(r'Time (s)')

    axs_steps[0].set_ylabel(r'Total power (MW)')
    axs_steps[1].set_ylabel(r'Frequency (Hz)')
    axs_steps[2].set_ylabel(r'Turbogenerators (MW)')
    axs_steps[3].set_ylabel(r'ESS (MW)')

    axs_steps[3].set_xticks(np.arange(0, 10, 1))
    axs_steps[3].set_xlim([0, 10])

    axs_steps[0].set_yticks(np.arange(40, 56, 4))
    axs_steps[0].set_ylim([39.8, 52])

    axs_steps[1].set_yticks(np.arange(45, 52, 1))
    axs_steps[1].set_ylim([47, 50.1])

    axs_steps[2].set_yticks(np.arange(42, 55, 1))
    axs_steps[2].set_ylim([43.9, 51])

    axs_steps[3].set_yticks(np.arange(0, 6, 1))
    axs_steps[3].set_ylim([-0.1, 4])

    axs_steps[0].legend(loc='best', frameon=False)
    axs_steps[1].legend(loc='best', frameon=False)
    # axs_steps[2].legend(loc='best', frameon=False)

    fig_steps.align_ylabels(axs_steps[:])
    fig_steps.tight_layout()
    fig_steps.show()
    fig_steps.savefig(figstepsname, format='pdf')

    plt.show()


#####################################################
# main
#####################################################
def main():
    print("#####################")
    print("Function name: ", main.__name__)

    plot_fmeas_from_csvs()
    # print("Nothing else done")


if __name__ == '__main__':
    main()
