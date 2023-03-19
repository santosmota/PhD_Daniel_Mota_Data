#################################################################
# Generates the Frequency figure
#   of the OMAE paper, but in the format of the Thesis
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

def plotchart ():

    ###############################################################
    # file path
    ###############################################################
    picture_folder = '../Modelos/ChHESS/'

    CSVs_path = '../Modelos/ChHESS/'

    raw_03_Freq_file_name = '20211206_Case03_Freq'
    raw_03_Freq_full_file_path = CSVs_path + raw_03_Freq_file_name + '.csv'

    save_file_name = 'HESSPowFacFreqGlobVar'
    save_full_file_path = picture_folder + save_file_name + '.pdf'


    ###############################################################
    # reading raw dados from csv files
    ################################################################
    print('Opening raw CSV file:')
    print(raw_03_Freq_full_file_path)
    dados_03_Freq = np.genfromtxt(raw_03_Freq_full_file_path, delimiter=',', skip_header=2)

    ###############################################################
    # Rated values
    ###############################################################
    # PCC_Volt_Nom_kV = 11.0

    # ESS_DCVolt_Nom_kV = 1.2

    # ESS_690V_Nom_kV = 0.69
    PCC_Freq_Nom_Hz = 50.0

    ###############################################################
    # hardcoded indexes for the variables
    ###############################################################
    #PCC data
    time = 0
    ESS_690V_f = 1
    WT1_690V_f = 2
    WT2_690V_f = 3
    WT3_690V_f = 4
    GG_01_speed = 5
    GG_02_speed = 6



    ###############################################################
    # non causal moving average (things I did before I new pandas)
    ################################################################
    avg_lados = 10
    #   |__|__|-2|-1| 0 |+1|+2|__|__|__|
    tamanho = len(dados_03_Freq[:, time])
    aux = np.zeros(tamanho)
    for i in range(avg_lados, tamanho - avg_lados - 1, 1):
        aux_sum = 0.0
        for k in range(-avg_lados, avg_lados + 1):
            aux_sum = aux_sum + dados_03_Freq[i + k, WT1_690V_f]
        aux[i] = aux_sum / (2 * avg_lados + 1)
    dados_03_Freq[avg_lados:-avg_lados - 1, WT1_690V_f] = aux[avg_lados:-avg_lados - 1]

    ##
    #avg_lados = 5
    aux = np.zeros(tamanho)
    for i in range(avg_lados, tamanho - avg_lados - 1, 1):
        aux_sum = 0.0
        for k in range(-avg_lados, avg_lados + 1):
            aux_sum = aux_sum + dados_03_Freq[i + k, WT2_690V_f]
        aux[i] = aux_sum / (2 * avg_lados + 1)
    dados_03_Freq[avg_lados:-avg_lados - 1, WT2_690V_f] = aux[avg_lados:-avg_lados - 1]

    ##
    #avg_lados = 2
    aux = np.zeros(tamanho)
    for i in range(avg_lados, tamanho - avg_lados - 1, 1):
        aux_sum = 0.0
        for k in range(-avg_lados, avg_lados + 1):
            aux_sum = aux_sum + dados_03_Freq[i + k, WT3_690V_f]
        aux[i] = aux_sum / (2 * avg_lados + 1)
    dados_03_Freq[avg_lados:-avg_lados - 1, WT3_690V_f] = aux[avg_lados:-avg_lados - 1]

    ##
    #avg_lados = 5
    aux = np.zeros(tamanho)
    for i in range(avg_lados, tamanho - avg_lados - 1, 1):
        aux_sum = 0.0
        for k in range(-avg_lados, avg_lados + 1):
            aux_sum = aux_sum + dados_03_Freq[i + k, ESS_690V_f]
        aux[i] = aux_sum / (2 * avg_lados + 1)
    dados_03_Freq[avg_lados:-avg_lados - 1, ESS_690V_f] = aux[avg_lados:-avg_lados - 1]

    ###########################
    ## Generators - Moving Average
    avg_lados = 1
    aux = np.zeros(tamanho)
    for i in range(avg_lados, tamanho - avg_lados - 1, 1):
        aux_sum = 0.0
        for k in range(-avg_lados, avg_lados + 1):
            aux_sum = aux_sum + dados_03_Freq[i + k, GG_01_speed]
        aux[i] = aux_sum / (2 * avg_lados + 1)
    dados_03_Freq[avg_lados:-avg_lados - 1, GG_01_speed] = aux[avg_lados:-avg_lados - 1]

    ##
    #avg_lados = 2
    aux = np.zeros(tamanho)
    for i in range(avg_lados, tamanho - avg_lados - 1, 1):
        aux_sum = 0.0
        for k in range(-avg_lados, avg_lados + 1):
            aux_sum = aux_sum + dados_03_Freq[i + k, GG_02_speed]
        aux[i] = aux_sum / (2 * avg_lados + 1)
    dados_03_Freq[avg_lados:-avg_lados - 1, GG_02_speed] = aux[avg_lados:-avg_lados - 1]



    ###############################################################
    # time shift
    ################################################################
    timeshift = 0
    ################################################################
    # caso 03 - PCC
    #find "timeshift" index
    k = 0
    aux = len(dados_03_Freq[:, time])
    for i in range(len(dados_03_Freq[:, time])):
        if dados_03_Freq[i, time] < timeshift:
            k = k + 1
    #delete points before timeshift
    dados_03_Freq = dados_03_Freq[k:None, :]
    #apply timeshift
    for i in range(len(dados_03_Freq[:, time])):
        dados_03_Freq[i, time] = dados_03_Freq[i, time] - timeshift

    ###############################################################
    # size of the figure
    ###############################################################
    figsizex = 5
    figsizey = 2.5

    ##################################################
    # the figure where the plots will be
    ##################################################
    fig, axs = plt.subplots(1, 1, sharex=True, figsize=(figsizex, figsizey))
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0.075, left=0.175, bottom=0.125, right=0.95, top=0.98)
    linewidth = 0.75

    #dados[:, time] = 1000 * dados[:, time]
    start_time = 0.5
    end_time = 2.5

    start_time_index = 0
    end_time_index = None

    #lightcolor = (0.7, 0.7, 0.7)

    ##################################################
    # DC link voltage
    ###################################################
    axs.plot(dados_03_Freq[start_time_index:end_time_index, time],
             dados_03_Freq[start_time_index:end_time_index, GG_01_speed] * PCC_Freq_Nom_Hz,
             color='black', linewidth=linewidth, linestyle='--', label=r'Speed GT1')

    axs.plot(dados_03_Freq[start_time_index:end_time_index, time],
             dados_03_Freq[start_time_index:end_time_index, GG_02_speed] * PCC_Freq_Nom_Hz,
             color='black', linewidth=linewidth, linestyle='-.', label=r'Speed GT2')

    axs.plot(dados_03_Freq[start_time_index:end_time_index, time],
             dados_03_Freq[start_time_index:end_time_index, ESS_690V_f] * PCC_Freq_Nom_Hz,
             color=pe.cor_dalt['red'], linewidth=linewidth, linestyle='-', label=r'Frequency ESS 690V')

    #axs.plot(dados_03_Freq[start_time_index:end_time_index, time],
    #         dados_03_Freq[start_time_index:end_time_index, WT1_690V_f],
    #         color='black', linewidth=linewidth+0.25, linestyle=':', label=r'Freq. WT1 690V')

    #axs.plot(dados_03_Freq[start_time_index:end_time_index, time],
    #         dados_03_Freq[start_time_index:end_time_index, WT2_690V_f],
    #         color='red', linewidth=linewidth, linestyle='-.', label=r'Freq. WT2 690V')

    axs.plot(dados_03_Freq[start_time_index:end_time_index, time],
             dados_03_Freq[start_time_index:end_time_index, WT3_690V_f] * PCC_Freq_Nom_Hz,
             color=pe.cor_dalt['blue'], linewidth=linewidth, linestyle='-', label=r'Frequency WT3 690V')

    ##################################################
    # Legends and titles
    #axs.set_xticks(np.arange(0, 10, 0.5))
    axs.set_xlim(start_time, end_time)
    #axs[0][1].set_xlim(start_time, end_time)

    axs.set_xlabel(r'Time (s)')

    axs.legend(loc='upper right', frameon=False)

    axs.set_ylabel(r'Speed and elect. freq. (Hz)')

    # axs.set_yticks(np.arange(0.997, 1, 0.0005))
    # axs.set_ylim(0.9973, 0.9997)

    axs.annotate("Sudden drop in\n electrical frequency is\n not mechanical.",
                 xy=(1.01, 0.9992 * PCC_Freq_Nom_Hz), xycoords='data',
                 xytext=(0.6, 0.9975 * PCC_Freq_Nom_Hz), textcoords='data',
                 arrowprops=dict(arrowstyle="->",
                connectionstyle="arc3"),
                 )

    axs.annotate("Mechanical and electrical frequency\n differ during transient.",
                 xy=(1.700136, 0.997807 * PCC_Freq_Nom_Hz ), xycoords='data',
                 xytext=(1.45, 0.99815 * PCC_Freq_Nom_Hz), textcoords='data',
                 arrowprops=dict(arrowstyle="->",
                connectionstyle="arc3"),
                 )

    fig.tight_layout()
    fig.align_ylabels(axs)

    ##################################################
    # saving and showing
    ##################################################
    print('Saving path and file:')
    print(save_full_file_path)
    plt.savefig(save_full_file_path, format='pdf')
    plt.show()

#####################################################
# main
#####################################################
def main():
    print("#####################")
    print("Function name: ", main.__name__)

    plotchart()

if __name__ == '__main__':
    main()