#################################################################
# Generates figure
# which contains the steps of 1.2MW with the Power Factory models
#   makes two charts on top of each other with voltage and frequency
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

#####################################################
# plot charts with voltage and frequency measurement from a set of csv files
#####################################################
def plot_vpcc_fmeas_from_csvs(simcount_total=7,
                              csvfolder="../Modelos/PrimReserveSharingPowFact/20220824",
                              offsetfrequency=False,
                              Fn=50.0,
                              timeoffset=0.0,
                              ):
    print("#####################")
    print("Function name: ", plot_vpcc_fmeas_from_csvs.__name__)

    ##########################################################################
    # figure
    ##########################################################################
    figsizex = 5
    figsizey = 3
    figstepsnamevpcc = csvfolder + '/ChFreq_Steps_1_2MW_PowFact.pdf'
    fig_steps_vpcc, axs_steps_vpcc = plt.subplots(2, 1, sharex=True,
                                                  figsize=(figsizex, figsizey),
                                                  num='StepFVpcc')

    ##########################################################################
    # style of the plots
    ##########################################################################
    cores = []
    legendas = []
    marker = []
    estilos = []
    for simcount in range(0, simcount_total, 1):
        if simcount == 0:
            cores.append('red')
            legendas.append('GTs')
            marker.append('x')
            estilos.append('-')  # , ':', '-.']
        elif simcount == 1:
            cores.append('gray')
            legendas.append('GTs+BTC+FLX')
            marker.append('+')
            estilos.append(':')
        elif simcount == simcount_total - 1:
            cores.append('blue')
            legendas.append('BTC+FLX')
            marker.append('*')
            estilos.append('-.')
        else:
            cores.append('gray')
            legendas.append('')
            marker.append('+')
            estilos.append(':')

    grossuras = 0.75
    markersize = 5

    ##########################################################################
    # plotting the eigen values
    ##########################################################################
    for simcount in range(0, simcount_total, 1):

        colname = "fmeas_0" + str(simcount)
        csvtimedomainname = csvfolder + "/timedomain_0" + str(simcount) + '.csv'

        df_td = pd.read_csv(csvtimedomainname)

        if offsetfrequency:
            df_td[colname] = df_td[colname] - (df_td[colname][0] - Fn)


        axs_steps_vpcc[0].plot(df_td['time'] + timeoffset,
                                   df_td['fmeasSEC'],
                                   linestyle=estilos[simcount],
                                   linewidth=grossuras,
                                   color=cores[simcount],
                                   label=legendas[simcount])
        axs_steps_vpcc[1].plot(df_td['time'] + timeoffset,
                                   df_td['vpcc'],
                                   linestyle=estilos[simcount],
                                   linewidth=grossuras,
                                   color=cores[simcount],
                                   label=legendas[simcount])

    ##########################################################################
    # axis names
    ##########################################################################
    axs_steps_vpcc[0].set_ylabel(r'Frequency (Hz)')

    axs_steps_vpcc[1].set_xlabel(r'Time (s)')
    axs_steps_vpcc[1].set_ylabel(r'Voltage (kV)')

    axs_steps_vpcc[1].set_xticks(np.arange(-20, 180, 1))
    axs_steps_vpcc[1].set_xlim([0, 8])

    axs_steps_vpcc[1].set_yticks(np.arange(10.0, 11.1, 0.01))
    axs_steps_vpcc[1].set_ylim([10.97, 11.0])

    corlegenda = 'whitesmoke'

    axs_steps_vpcc[0].annotate(r'a', xy=(0.0625, 0.2), xycoords='axes fraction',
                                   bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps_vpcc[1].annotate(r'b', xy=(0.0625, 0.2), xycoords='axes fraction',
                                   bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps_vpcc[1].legend(loc='lower right', frameon=False)

    fig_steps_vpcc.tight_layout()
    fig_steps_vpcc.show()

    fig_steps_vpcc.savefig(figstepsnamevpcc, format='pdf')

    plt.show()


#####################################################
# main
#####################################################
def main():
    print("#####################")
    print("Function name: ", main.__name__)

    plot_vpcc_fmeas_from_csvs(simcount_total=7,
                              offsetfrequency=False,
                              timeoffset=1.0,
                              )  # False, True

if __name__ == '__main__':
    main()

