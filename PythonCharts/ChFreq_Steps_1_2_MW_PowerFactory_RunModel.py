##############################################################################################
# Python functions for running a 1.2MW step and making CSVs
###############################################################################################
# By: Daniel dos Santos Mota, 2023-01-23
# 	This file has been copied from a private repository into this public one.
#       Some comments have been added only to the copied file.
#	It has not been tested after copying.
###############################################################################################

from tkinter import Tk  # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

import numpy as np

import powerfactorycontrol as pfc
import plothelp as pth

import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
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


##############################################################################
#  run_sim_steps_load_Z2_eigen
##############################################################################
def run_sim_steps_load_Z2_eigen(Z2_plini=1.0):
    print("#####################")
    print("Function name: ", run_sim_steps_load_Z2_eigen.__name__)

    ##########################################################################
    # Open Power Factory
    ##########################################################################
    import sys
    sys.path.append(r"C:\programs\DIgSILENT\PowerFactory-2020\Python\3.7")
    # Path to PowerFactory Python Module
    # for name in sys.path:
    #    print(name)
    import powerfactory as pf

    app = pf.GetApplication()
    if app is None:
        raise Exception('getting Powerfactory application failed')

    proj_name = '202208_RMS_Tests'
    study_case = 'Study Case'
    project, proj = pfc.open_project_study_case(app=app,
                                                proj_name=proj_name,
                                                study_case=study_case)
    ##########################################################################
    # folder for saving the csv files
    ##########################################################################
    csvfolder = "../Powerfactory/simdata/20220824/"
    csveigentotfolder = '\\\\!REDACTED!\\2022_Journal_Data\\Powerfactory\\simdata\\20220824\\'

    figstepname = csvfolder + '/figsteps_needsretouching.eps'
    figeigename = csvfolder + '/figeigen_needsretouching.eps'
    figstep11kVname = csvfolder + '/figsteps11kV_needsretouching.eps'

    ##########################################################################
    # Figures for plotting
    ##########################################################################
    figsizex = 4
    figsizey = 2
    fig_steps, axs_steps = plt.subplots(1, 1, sharex=True,
                                        figsize=(figsizex, figsizey),
                                        num='Step')

    fig_steps_BTC, axs_steps_BTC = plt.subplots(1, 1, sharex=True,
                                                figsize=(figsizex, figsizey),
                                                num='StepBTC')

    fig_steps_11kV, axs_steps_11kV = plt.subplots(1, 1, sharex=True,
                                                  figsize=(figsizex, figsizey),
                                                  num='Step11kV')

    figsizex = 5
    figsizey = 9
    fig_eigen, axs_eigen = plt.subplots(1, 1, sharex=True,
                                        figsize=(figsizex, figsizey),
                                        num='Eigen')

    cores = ['red', 'gray', 'gray', 'gray', 'gray', 'gray', 'blue']
    estilos = ['-', ':', ':', ':', ':', ':', '-.']
    legendas = ['GTs only', '', '', '', '', '', 'ESS only']

    grossuras = 0.75
    marker = 'x'
    markersize = 5

    ##########################################################################
    # parameters for each run
    ##########################################################################
    N_db = 0.0

    gts_normal_k = np.array([6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0]) * 50.0 / 35.2
    gts_max_normal_droop_power = 1.5 / 35.2
    gts_min_normal_droop_power = -1.5 / 35.2

    btc_kp_gain = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]) * 50.0 / 1.54
    btc_max_normal_droop_power = 1.5 / 1.54
    btc_min_normal_droop_power = -1.5 / 1.54

    flex_kp_gain = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]) * 50.0 / (7.6 / 0.9)
    flex_max_normal_droop_power = 1.5 / (7.6 / 0.9)
    flex_min_normal_droop_power = -1.5 / (7.6 / 0.9)

    simcount_total = 7

    ##########################################################################
    # Set transient : connection of Load Z2 at time 155s
    ##########################################################################
    t_to_steady_state = 30
    t_transient = t_to_steady_state + 10
    t_middle_eigen = t_transient + 20

    pfc.set_load_param(app, load_name='Z2.ElmLod',
                       input_mode='PC',  # DEF: default, PC: P, cos(phi)
                       plini=Z2_plini,  # active power in MW
                       coslini=0.95,  # cosinus phi
                       pf_recap=0,  # 0: ind          1: cap
                       u0=1.0)  # rated voltage in pu

    pfc.set_switch_transient_param(app, trans_name='PCC11kVZ2',
                                   outserv=0,  # 0: in service       1: out of service
                                   time=t_transient,  # time of the transient in seconds
                                   i_switch=1,  # 0:open              1: close
                                   i_allph=1)  # 0:not all phases    1: all phases

    for simcount in range(0, simcount_total, 1):
        print("######################################################")
        print("Simulation run: ", simcount, "of ", simcount_total - 1)
        ##########################################################################
        # droops
        ##########################################################################
        pfc.set_iactrefgen_droop(app, controller_name='BCiactref.ElmDsl',
                                 ferrdb=N_db,
                                 kp=btc_kp_gain[simcount],
                                 pdroopmax=btc_max_normal_droop_power,
                                 pdroopmin=btc_min_normal_droop_power)

        pfc.set_iactrefgen_droop(app, controller_name='FLEX_iact_ref_gen.ElmDsl',
                                 ferrdb=N_db,
                                 kp=flex_kp_gain[simcount],
                                 pdroopmax=flex_max_normal_droop_power,
                                 pdroopmin=flex_min_normal_droop_power)

        pfc.set_govdb_N_droop(app, controller_name='GT1govdb.ElmDsl',
                              db_normal=N_db,
                              kN=gts_normal_k[simcount],
                              deltaP_normal_max=gts_max_normal_droop_power,
                              deltaP_normal_min=gts_min_normal_droop_power)

        pfc.set_govdb_N_droop(app, controller_name='GT2govdb.ElmDsl',
                              db_normal=N_db,
                              kN=gts_normal_k[simcount],
                              deltaP_normal_max=gts_max_normal_droop_power,
                              deltaP_normal_min=gts_min_normal_droop_power)

        ##########################################################################
        # run for steady state and run model analysis
        ##########################################################################
        pfc.calc_ini_rms(app=app)
        pfc.run_rms(app=app, tstop=t_to_steady_state)
        pfc.save_snapshot(app=app)

        ##########################################################################
        # purposefully re-initiate, load snapshot, run simulation, to drop the first 150s of the results
        ##########################################################################
        pfc.calc_ini_rms(app=app)
        pfc.load_snapshot(app=app)

        ##########################################################################
        # names for the csv and for the columns of the dataframe (time domain, to be created later)
        ##########################################################################

        if simcount < 10:
            csvname = csvfolder + "/eigenvalues_0" + str(simcount) + '.csv'
            csvtimedomainname = csvfolder + "/timedomain_0" + str(simcount) + '.csv'

            # colname = "fmeas_0" + str(simcount)
            csveigentotname = csveigentotfolder + 'eigenvalues_total_0' + str(simcount) + '.csv'  #
        else:
            csvname = csvfolder + "/eigenvalues_" + str(simcount) + '.csv'
            csvtimedomainname = csvfolder + "/timedomain_" + str(simcount) + '.csv'

            # colname = "fmeas_" + str(simcount)
            csveigentotname = csveigentotfolder + 'eigenvalues_total_' + str(simcount) + '.csv'

        ##########################################################################
        # run step, calculate modal, create dataframe (eigen values)
        ##########################################################################
        pfc.run_rms(app=app, tstop=t_middle_eigen)
        pfc.run_modal(app=app)
        eigen_real, eigen_imag, eigen_part_names = pfc.get_eigen_real_imag_participation(app=app,
                                                                                         part_threshold=0.5,
                                                                                         include_states_in_names=False,
                                                                                         add_partfact_to_name=True,
                                                                                         savetotaleigen=True,
                                                                                         csveigentotname=csveigentotname)

        df_eigen = pd.DataFrame({"real": eigen_real,
                                 "imag": eigen_imag,
                                 "names": eigen_part_names})

        ##########################################################################
        # erase eigen values from AM_loads, saves csv for post processing of charts
        ##########################################################################
        df_eigen = df_eigen[
            ~df_eigen['names'].str.contains("AM_")]  # deletes eigenvalues with AM_ loads which are not active
        df_eigen.to_csv(csvname, index=False)

        ##########################################################################
        # plots eigen values, aux lines, and names
        ##########################################################################
        axs_eigen.plot(df_eigen['real'], df_eigen['imag'],
                       color=cores[simcount],
                       label=legendas[simcount],
                       linestyle='None',
                       linewidth=grossuras,
                       marker=marker,
                       markersize=markersize)

        if simcount == 0:
            pth.plot_root_locus_damping_lines(eigen_real=df_eigen['real'],
                                              eigen_imag=df_eigen['imag'],
                                              axis=axs_eigen, nzetalines=31)

        if simcount == 0 or simcount == simcount_total - 1:
            pth.add_root_locus_part_names(eigen_real=df_eigen['real'],
                                          eigen_imag=df_eigen['imag'],
                                          eigen_part_names=df_eigen['names'],
                                          axis=axs_eigen,
                                          zeta_threshold=0.98)

        ##########################################################################
        # retrieve time domain data
        ##########################################################################
        elmRes = app.GetFromStudyCase('*.ElmRes')  # get the result file
        elmRes.Load()  # load the result file in memory
        n_row = elmRes.GetNumberOfRows()  # get the number of samples

        time = pfc.get_res_time(app=app, elmres=elmRes)
        time = pth.time_offset(time, offset=-t_transient)

        df_td = pd.DataFrame({"time": time})

        fmeas = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                    element_name='PLATPsecctrl.ElmDsl',
                                    signal_name='s:Fmeas')

        fmeasBTC = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                       element_name='BCiactref.ElmDsl',
                                       signal_name='s:Fmeas')

        vpcc = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                   element_name='PCC11kvmeas.StaVmea',
                                   signal_name='s:u')

        df_td['fmeasSEC'] = fmeas
        df_td['fmeasBTC'] = fmeasBTC
        df_td['vpcc'] = vpcc * 11.0

        axs_steps.plot(df_td['time'],
                       df_td['fmeasSEC'],
                       linestyle=estilos[simcount],
                       linewidth=grossuras,
                       color=cores[simcount],
                       label=legendas[simcount])

        axs_steps_BTC.plot(df_td['time'],
                           df_td['fmeasBTC'],
                           linestyle=estilos[simcount],
                           linewidth=grossuras,
                           color=cores[simcount],
                           label=legendas[simcount])

        axs_steps_11kV.plot(df_td['time'],
                            df_td['vpcc'],
                            linestyle=estilos[simcount],
                            linewidth=grossuras,
                            color=cores[simcount],
                            label=legendas[simcount])

        df_td.to_csv(csvtimedomainname, index=False)

    ##########################################################################
    # axis names
    ##########################################################################
    axs_steps.set_xlabel(r'Time (s)')
    axs_steps.set_ylabel(r'Frequency (Hz)')

    axs_steps_BTC.set_xlabel(r'Time (s)')
    axs_steps_BTC.set_ylabel(r'Frequency (Hz)')

    axs_steps.set_xticks(np.arange(-20, 180, 5))
    axs_steps.set_xlim([-10, 20])

    axs_steps_BTC.set_xticks(np.arange(-20, 180, 5))
    axs_steps_BTC.set_xlim([-10, 20])

    axs_steps.legend(loc='best', frameon=True)
    axs_steps_BTC.legend(loc='best', frameon=True)

    axs_eigen.set_xlabel(r'Real (Np/s)')
    axs_eigen.set_ylabel(r'Imaginary (rad/s)')

    fig_steps.tight_layout()
    fig_steps_BTC.tight_layout()
    fig_steps_11kV.tight_layout()

    fig_steps_11kV.show()
    fig_steps_11kV.savefig(figstep11kVname, format='eps')

    fig_steps.show()
    fig_steps.savefig(figstepname, format='eps')

    fig_eigen.tight_layout()
    fig_eigen.show()
    fig_eigen.savefig(figeigename, format='eps')

    plt.show()



#####################################################
# main
#####################################################
def main():
    print("#####################")
    print("Function name: ", main.__name__)

    run_sim_steps_load_Z2_eigen(Z2_plini=1.2)
    # ON the day 20220818
    # PLATPsecctrl kg = 1, Toff = 60s


if __name__ == '__main__':
    main()

