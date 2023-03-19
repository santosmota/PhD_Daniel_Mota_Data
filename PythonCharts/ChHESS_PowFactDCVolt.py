#################################################################
# Generates the DC voltage figure
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

    raw_03_ESS_file_name = '20211206_Case03_ESS'
    raw_03_ESS_full_file_path = CSVs_path + raw_03_ESS_file_name + '.csv'

    # raw_03_PCC_file_name = '20211206_Case03_PCC'
    # raw_03_PCC_full_file_path = CSVs_path + raw_03_PCC_file_name + '.csv'

    raw_04_ESS_file_name = '20211206_Case04_ESS'
    raw_04_ESS_full_file_path = CSVs_path + raw_04_ESS_file_name + '.csv'

    # raw_04_PCC_file_name = '20211206_Case04_PCC'
    # raw_04_PCC_full_file_path = CSVs_path + raw_04_PCC_file_name + '.csv'

    save_file_name = 'HESSPowFacDCVolt'
    save_full_file_path = picture_folder + save_file_name + '.pdf'

    ###############################################################
    # reading raw dados from csv files
    ################################################################
    print('Opening raw CSV file:')
    print(raw_03_ESS_full_file_path)
    dados_03_ESS = np.genfromtxt(raw_03_ESS_full_file_path, delimiter=',', skip_header=2)

    # print('Opening raw CSV file:')
    # print(raw_03_PCC_full_file_path)
    # dados_03_PCC = np.genfromtxt(raw_03_PCC_full_file_path, delimiter=',', skip_header=2)

    print('Opening raw CSV file:')
    print(raw_04_ESS_full_file_path)
    dados_04_ESS = np.genfromtxt(raw_04_ESS_full_file_path, delimiter=',', skip_header=2)

    # print('Opening raw CSV file:')
    # print(raw_04_PCC_full_file_path)
    # dados_04_PCC = np.genfromtxt(raw_04_PCC_full_file_path, delimiter=',', skip_header=2)

    ###############################################################
    # Rated values
    ###############################################################
    # PCC_Volt_Nom_kV = 11.0

    ESS_DCVolt_Nom_kV = 1.2

    # ESS_690V_Nom_kV = 0.69

    # BC_DCLinkSide_Inom_kA = 3.5
    # FC_DCLinkSide_Inom_kA = 5.0
    # ESS_GC_Idcnom_kA = -10.0/1.2

    ###############################################################
    # hardcoded indexes for the variables
    ###############################################################
    #ESS_GC,ESS_GC,BC_DCLinkSide,FC_DCLinkSide
    #"Time in s",
    # "Output Voltage, Absolute in p.u.",
    # "Power-Phasor, Active Power/Terminal AC in MW",
    # "Active Power in p.u.",
    # "DC-voltage in p.u.",
    # "DC-current in p.u.",
    # "DC Current Input in p.u.","DC Current Input in p.u."

    #ESS data
    time = 0
    ESS_690V_u_pu = 1
    ESS_GC_p_MW = 2
    BC_DCLinkSide_p_MW = 3
    ESS_GC_Udc_pu = 4
    ESS_GC_Idc_pu = 5
    BC_DCLinkSide_i_pu = 6
    FC_DCLinkSide_i_pu = 7

    #PCC data
    # GG_01_speed = 1
    # GG_02_speed = 2
    # GG01_p_MW = 3
    # GG02_p_MW = 4
    # RL01_11kV_p_MW = 5
    # RL02_11kV_p_MW = 6
    # WF_11kV_p_MW = 7
    # ESS_TR_11kV_p_MW = 8
    # LV_Load_11kV_p_MW = 9
    # WT1_33kV_p_MW = 10
    # WT2_33kV_p_MW = 11
    # WT3_33kV_p_MW = 12
    # GG_01_u_pu = 13

    ###############################################################
    # time shift
    ################################################################
    timeshift = 0
    ###############################################################
    # size of the figure
    ###############################################################
    figsizex = 5
    figsizey = 2

    ##################################################
    # the figure where the plots will be
    ##################################################
    fig, axs = plt.subplots(1, 1, sharex=True, figsize=(figsizex, figsizey))
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0.075, left=0.175, bottom=0.125, right=0.95, top=0.98)
    linewidth = 0.75

    #dados[:, time] = 1000 * dados[:, time]
    start_time = 0
    end_time = 3

    start_time_index = 0
    end_time_index = None

    #lightcolor = (0.7, 0.7, 0.7)

    ##################################################
    # DC link voltage
    ###################################################
    axs.plot(dados_03_ESS[start_time_index:end_time_index, time],
                    dados_03_ESS[start_time_index:end_time_index, ESS_GC_Udc_pu] * ESS_DCVolt_Nom_kV,
                    color=pe.cor_dalt['blue'], linewidth=linewidth, linestyle='-', label=r'With $i_{es}$ feed forward')

    axs.plot(dados_04_ESS[start_time_index:end_time_index, time],
                    dados_04_ESS[start_time_index:end_time_index, ESS_GC_Udc_pu] * ESS_DCVolt_Nom_kV,
                    color=pe.cor_dalt['red'], linewidth=linewidth, linestyle='-', label=r'Without $i_{es}$ feed forward')

    ##################################################
    # Legends and titles
    axs.set_xticks(np.arange(0, 10, 0.5))

    axs.set_xlim(start_time, end_time)
    #axs[0][1].set_xlim(start_time, end_time)

    axs.set_xlabel(r'Time (s)')

    axs.legend(loc='upper right', frameon=False)

    axs.set_ylabel(r'DC voltage (kV)')

    #axs[2].set_yticks(np.arange(0, 1, 0.025))
    #axs[2].set_ylim(0.997, 1.003)

    #axs.annotate(r'Nadir',
                #xy=(12.692, 0.9805), xycoords='data',
                #xytext=(20, 0.9805), textcoords='data',
                #arrowprops=dict(arrowstyle="->",
                #connectionstyle="arc3"),
                #)

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
