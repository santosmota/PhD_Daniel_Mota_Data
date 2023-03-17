#################################################################
# Generates the big figure
#   of the OMAE paper again
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
    # C:\Users\danielmo\OneDrive - SINTEF\Documents\GitHub\PhD_Daniel_Mota_Data
    # '../Modelos/ChHESS/
    picture_folder = '../Modelos/ChHESS/'

    CSVs_path = '../Modelos/ChHESS/'

    #raw_01_file_name = '20211201_Case01_PCC'
    raw_01_file_name = '20211206_Case01_PCC'
    raw_01_full_file_path = CSVs_path + raw_01_file_name + '.csv'

    #raw_02_file_name = '20211201_Case02_PCC_DroopInt_NoDeriv'
    raw_02_file_name = '20211206_Case02_PCC'
    raw_02_full_file_path = CSVs_path + raw_02_file_name + '.csv'

    #raw_03_file_name = '20211201_Case03_PCC_DroopInt_Deriv'
    raw_03_file_name = '20211206_Case03_PCC'
    raw_03_full_file_path = CSVs_path + raw_03_file_name + '.csv'

    #raw_04_file_name = '20211201_Case04_PCC_DroopInt_Deriv_NoFFwrd'
    #raw_04_full_file_path = CSVs_path + raw_04_file_name + '.csv'

    save_file_name = 'HESSPowFacFreq'
    save_full_file_path = picture_folder + save_file_name + '.pdf'

    ###############################################################
    # reading raw dados from csv files
    ################################################################
    print('Opening raw CSV file:')
    print(raw_01_full_file_path)
    dados_01 = np.genfromtxt(raw_01_full_file_path, delimiter=',', skip_header=2)

    print('Opening raw CSV file:')
    print(raw_02_full_file_path)
    dados_02 = np.genfromtxt(raw_02_full_file_path, delimiter=',', skip_header=2)

    print('Opening raw CSV file:')
    print(raw_03_full_file_path)
    dados_03 = np.genfromtxt(raw_03_full_file_path, delimiter=',', skip_header=2)

    #LV_Load_MW = 1.1 #low voltage load that was not included in the simulations... might be included later
    PCC_Volt_Nom_kV = 11.0

    ###############################################################
    # hardcoded indexes for the variables
    ################################################################
    #PCC data
    time = 0
    GG_01_speed = 1
    GG_02_speed = 2
    GG01_p_MW = 3
    GG02_p_MW = 4
    RL01_11kV_p_MW = 5
    RL02_11kV_p_MW = 6
    WF_11kV_p_MW = 7
    ESS_TR_11kV_p_MW = 8
    LV_Load_11kV_p_MW = 9
    WT1_33kV_p_MW = 10
    WT2_33kV_p_MW = 11
    WT3_33kV_p_MW = 12
    GG_01_u_pu = 13

    ###############################################################
    # time shift
    ################################################################
    timeshift = 0

    ################################################################
    # caso 01 -
    #find "timeshift" index
    k = 0
    aux = len(dados_01[:, time])
    for i in range(len(dados_01[:, time])):
        if dados_01[i, time] < timeshift:
            k = k + 1
    #delete points before timeshift
    dados_01 = dados_01[k:None, :]
    #apply timeshift
    for i in range(len(dados_01[:, time])):
        dados_01[i, time] = dados_01[i, time] - timeshift

    ################################################################
    # caso 02 -
    #find "timeshift" index
    k = 0
    aux = len(dados_02[:, time])
    for i in range(len(dados_02[:, time])):
        if dados_02[i, time] < timeshift:
            k = k + 1
    #delete points before timeshift
    dados_02 = dados_02[k:None, :]
    #apply timeshift
    for i in range(len(dados_02[:, time])):
        dados_02[i, time] = dados_02[i, time] - timeshift

    ################################################################
    # caso 03 -
    #find "timeshift" index
    k = 0
    aux = len(dados_03[:, time])
    for i in range(len(dados_03[:, time])):
        if dados_03[i, time] < timeshift:
            k = k + 1
    #delete points before timeshift
    dados_03 = dados_03[k:None, :]
    #apply timeshift
    for i in range(len(dados_03[:, time])):
        dados_03[i, time] = dados_03[i, time] - timeshift


    ###############################################################
    # size of the figure
    ###############################################################
    # cm = 1/2.54
    # figsizex = 11.5 * cm
    # figsizey = 17 * cm
    figsizex = 5
    figsizey = 7.5

    ##################################################
    # the figure where the plots will be
    ##################################################
    fig, axs = plt.subplots(6, 1, sharex=True, figsize=(figsizex, figsizey))
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0.075, left=0.175, bottom=0.125, right=0.95, top=0.98)
    linewidth = 0.75

    #dados[:, time] = 1000 * dados[:, time]
    start_time = 0
    end_time = 6

    start_time_index = 0
    end_time_index = None

    #lightcolor = (0.7, 0.7, 0.7)

    ##################################################
    # Total Electrical Load
    ##################################################
    axs[0].plot(dados_01[start_time_index:end_time_index, time],
                    dados_01[start_time_index:end_time_index, RL01_11kV_p_MW] +
                    dados_01[start_time_index:end_time_index, RL02_11kV_p_MW] +
                    dados_01[start_time_index:end_time_index, LV_Load_11kV_p_MW],
                    color='green', linewidth=linewidth, linestyle='-', label=r'Case 1: no ESS support')

    axs[0].plot(dados_02[start_time_index:end_time_index, time],
                    dados_02[start_time_index:end_time_index, RL01_11kV_p_MW] +
                    dados_02[start_time_index:end_time_index, RL02_11kV_p_MW] +
                    dados_02[start_time_index:end_time_index, LV_Load_11kV_p_MW],
                    color=pe.cor_dalt['red'], linewidth=linewidth, linestyle='-', label=r'Case 2: ESS Primary')

    axs[0].plot(dados_03[start_time_index:end_time_index, time],
                   dados_03[start_time_index:end_time_index, RL01_11kV_p_MW] +
                   dados_03[start_time_index:end_time_index, RL02_11kV_p_MW] +
                   dados_03[start_time_index:end_time_index, LV_Load_11kV_p_MW],
                   color=pe.cor_dalt['blue'], linewidth=linewidth, linestyle='-', label=r'Case 3: ESS Primary+Inertia')


    ##################################################
    # Speed
    ##################################################
    axs[1].plot(dados_01[start_time_index:end_time_index, time],
             dados_01[start_time_index:end_time_index, GG_01_speed]*50.0,
             color=pe.cor_dalt['green'], linewidth=linewidth, linestyle='-', label=r'No ESS')

    axs[1].plot(dados_02[start_time_index:end_time_index, time],
             dados_02[start_time_index:end_time_index, GG_01_speed]*50.0,
             color=pe.cor_dalt['red'], linewidth=linewidth, linestyle='-', label=r'ESS Droop')

    axs[1].plot(dados_03[start_time_index:end_time_index, time],
             dados_03[start_time_index:end_time_index, GG_01_speed]*50.0,
             color=pe.cor_dalt['blue'], linewidth=linewidth, linestyle='-', label=r'ESS Droop, Deriv.')

    ##################################################
    # Gen Power
    ##################################################
    axs[2].plot(dados_01[start_time_index:end_time_index, time],
                    dados_01[start_time_index:end_time_index, GG01_p_MW] +
                    dados_01[start_time_index:end_time_index, GG02_p_MW],
                    color=pe.cor_dalt['green'], linewidth=linewidth, linestyle='-', label=r'No ESS')

    axs[2].plot(dados_02[start_time_index:end_time_index, time],
                    dados_02[start_time_index:end_time_index, GG01_p_MW] +
                    dados_02[start_time_index:end_time_index, GG02_p_MW],
                    color=pe.cor_dalt['red'], linewidth=linewidth, linestyle='-', label=r'ESS Droop')

    axs[2].plot(dados_03[start_time_index:end_time_index, time],
                   dados_03[start_time_index:end_time_index, GG01_p_MW] +
                   dados_03[start_time_index:end_time_index, GG02_p_MW],
                   color=pe.cor_dalt['blue'], linewidth=linewidth, linestyle='-', label=r'ESS Droop, Deriv.')

    ##################################################
    # Wind Power
    ##################################################
    axs[4].plot(dados_01[start_time_index:end_time_index, time],
                    dados_01[start_time_index:end_time_index, WF_11kV_p_MW],
                    color=pe.cor_dalt['green'], linewidth=linewidth, linestyle='-', label=r'No ESS')

    axs[4].plot(dados_02[start_time_index:end_time_index, time],
                    dados_02[start_time_index:end_time_index, WF_11kV_p_MW],
                    color=pe.cor_dalt['red'], linewidth=linewidth, linestyle='-', label=r'ESS Droop')

    axs[4].plot(dados_03[start_time_index:end_time_index, time],
                   dados_03[start_time_index:end_time_index, WF_11kV_p_MW],
                   color=pe.cor_dalt['blue'], linewidth=linewidth, linestyle='-', label=r'ESS Droop, Deriv')

    ##################################################
    # ESS
    ##################################################
    #axs[0][2].plot(dados_01[start_time_index:end_time_index, time],
    #                dados_01[start_time_index:end_time_index, ESS_TR_11kV_p_MW],
    #                color=pe.cor_dalt['green'], linewidth=linewidth, linestyle='-', label=r'No ESS')

    axs[3].plot(dados_02[start_time_index:end_time_index, time],
                    dados_02[start_time_index:end_time_index, ESS_TR_11kV_p_MW],
                    color=pe.cor_dalt['red'], linewidth=linewidth, linestyle='-', label=r'ESS Droop')

    axs[3].plot(dados_03[start_time_index:end_time_index, time],
                   dados_03[start_time_index:end_time_index, ESS_TR_11kV_p_MW],
                   color=pe.cor_dalt['blue'], linewidth=linewidth, linestyle='-', label=r'ESS Droop, Deriv')

    ##################################################
    # PCC voltage
    ##################################################
    axs[5].plot(dados_01[start_time_index:end_time_index, time],
                    dados_01[start_time_index:end_time_index, GG_01_u_pu] * PCC_Volt_Nom_kV,
                    color=pe.cor_dalt['green'], linewidth=linewidth, linestyle='-', label=r'No ESS')

    axs[5].plot(dados_02[start_time_index:end_time_index, time],
                    dados_02[start_time_index:end_time_index, GG_01_u_pu] * PCC_Volt_Nom_kV,
                    color=pe.cor_dalt['red'], linewidth=linewidth, linestyle='-', label=r'ESS Droop')

    axs[5].plot(dados_03[start_time_index:end_time_index, time],
                   dados_03[start_time_index:end_time_index, GG_01_u_pu] * PCC_Volt_Nom_kV,
                   color=pe.cor_dalt['blue'], linewidth=linewidth, linestyle='-', label=r'ESS Droop, Deriv')



    ##################################################
    # Legends and titles
    axs[0].set_xticks(np.arange(0, 10, 1))

    axs[0].set_xlim(start_time, end_time)
    #axs[0][1].set_xlim(start_time, end_time)

    #axs[1][0].set_xlabel(r'Time (s)')
    #axs[1][1].set_xlabel(r'Time (s)')
    axs[5].set_xlabel(r'Time (s)')

    axs[0].legend(loc='lower right', frameon=False)
    #axs[1][0].legend(loc='center right', frameon=False)

    axs[0].set_yticks(np.arange(45, 50, 1))
    axs[0].set_ylim(45, 49)

    axs[2].set_yticks(np.arange(32, 39, 1))
    axs[2].set_ylim(33, 38)

    axs[3].set_yticks(np.arange(-1, 2, 0.5))
    axs[3].set_ylim(-0.5, 1.7)

    axs[0].set_ylabel(r'Electr. load (MW)')
    axs[2].set_ylabel(r'Gen. power (MW)')
    #axs[1].set_ylabel(r'Gen. speed (pu)')
    axs[1].set_ylabel(r'Gen. speed (Hz)')
    axs[4].set_ylabel(r'Wind power (MW)')
    axs[3].set_ylabel(r'ESS power (MW)')
    axs[5].set_ylabel(r'Busbar volt. (kV)')

    #axs[2].set_yticks(np.arange(0, 1, 0.025))
    #axs[2].set_ylim(0.997, 1.003)


    ##################################################
    # LEGENDS
    ##################################################
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    # colors lightgray gray aliceblue whitesmoke
    corlegenda = 'whitesmoke'

    #axs[0][0].annotate(r'\textbf{(a.1)}}',
    #            xytext=(0, 0.35), textcoords='data',
    #            )
    axs[0].annotate(r'a', xy=(0.5, 48), xycoords='data',
                      va='center',
                      ha='center',
                      bbox=dict(boxstyle='circle', fc=corlegenda))

    axs[1].annotate(r'b', xy=(0.5, 49.9), xycoords='data',  # xy=(0.5, 0.998)
                      va='center',
                      ha='center',
                      bbox=dict(boxstyle='circle', fc=corlegenda))

    axs[3].annotate(r'd', xy=(0.5, 1), xycoords='data',
                      va='center',
                      ha='center',
                      bbox=dict(boxstyle='circle', fc=corlegenda))

    axs[4].annotate(r'e', xy=(0.5, 11.85), xycoords='data',
                      va='center',
                      ha='center',
                      bbox=dict(boxstyle='circle', fc=corlegenda))

    axs[2].annotate(r'c', xy=(0.5, 37), xycoords='data',
                      va='center',
                      ha='center',
                      bbox=dict(boxstyle='circle', fc=corlegenda))

    axs[5].annotate(r'f', xy=(0.5, 11), xycoords='data',
                      va='center',
                      ha='center',
                      bbox=dict(boxstyle='circle', fc=corlegenda))


    # https://matplotlib.org/stable/tutorials/text/annotations.html#id5
    ##################################################
    # anotation
    ##################################################
    axs[1].annotate(r'with ESS droop',
                xy=(5.510740, 49.89375), xycoords='data',  # xy=(5.510740, 0.997875), xycoords='data',
                xytext=(3.5, 49.95), textcoords='data',  # xytext=(3.5, 0.999), textcoords='data',
                arrowprops=dict(arrowstyle="->",
                connectionstyle="arc3"),
                )

    axs[1].annotate(r'ESS inertia',
                xy=(1.604659, 49.88785), xycoords='data',  # xy=(1.604659, 0.997757), xycoords='data',
                xytext=(1.5, 49.95), textcoords='data',  # xytext=(1.5, 0.999), textcoords='data',
                arrowprops=dict(arrowstyle="->",
                connectionstyle="arc3"),
                )

    axs[1].annotate(r'Generators alone, no ESS.',
                xy=(2.503226, 49.86), xycoords='data',  # xy=(2.503226, 0.9972), xycoords='data',
                xytext=(3, 49.825), textcoords='data',  # xytext=(3, 0.9965), textcoords='data',
                arrowprops=dict(arrowstyle="->",
                connectionstyle="arc3"),
                )

    axs[2].annotate('Generators take less load during the transient,\n due to ESS droop.',
                xy=(3.502959, 36.2), xycoords='data',
                xytext=(2.0, 33.2), textcoords='data',
                arrowprops=dict(arrowstyle="->",
                connectionstyle="arc3"),
                )

    axs[5].annotate('Room for improvement, if ESS voltage \n support implemented.',
                xy=(1.253061, (0.995662+0.001) * PCC_Volt_Nom_kV), xycoords='data',
                xytext=(2, 1.0024 * PCC_Volt_Nom_kV), textcoords='data',
                arrowprops=dict(arrowstyle="->",
                connectionstyle="arc3"),
                )

    axs[4].annotate('Wind farm\n reacts to voltage dip.',
                xy=(1.5, 11.75), xycoords='data',
                xytext=(1.5, 11.825), textcoords='data',
                arrowprops=dict(arrowstyle="->",
                connectionstyle="arc3"),
                )

    axs[3].annotate('ESS droop,\n proportional regulator.',
                xy=(5.005039, 0.740581), xycoords='data',
                xytext=(3.5, -0.2), textcoords='data',
                arrowprops=dict(arrowstyle="->",
                connectionstyle="arc3"),
                )

    axs[3].annotate('ESS inertia,\n derivative regulator.',
                xy=(1.604659, 1.294973), xycoords='data',
                xytext=(3, 1), textcoords='data',
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
