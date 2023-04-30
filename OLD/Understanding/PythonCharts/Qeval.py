#ABANDONADO!

###############################################################
# matplotlib
###############################################################
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['DejaVu Sans']})
rc('text', usetex=True)
params = {'text.latex.preamble': [r'\usepackage{amsmath}']}
plt.rcParams.update(params)

###############################################################
# numpy and scipy
###############################################################
import numpy as np

###############################################################
# select the time scale of the graphs - uncomment the time scales
###############################################################
figsizex = 5
figsizey = 3.5



###############################################################
# file path
###############################################################
picture_folder = 'Qeval/'

simulation_path = 'C:/Users/daniemot/OneDrive - NTNU/Publications/2021_PosNegSequences/matlab/Basics/'

raw_data_file_name_01 = 'Quality_01.txt'
raw_data_file_name_02 = 'Quality_05.txt'
raw_data_file_name_03 = 'Quality_10.txt'

raw_data_file_path_01 = simulation_path + raw_data_file_name_01
raw_data_file_path_02 = simulation_path + raw_data_file_name_02
raw_data_file_path_03 = simulation_path + raw_data_file_name_03

save_path = simulation_path + picture_folder + 'Comparison' + '.eps'

###############################################################
# reading data from csv files
################################################################
print('Opening files:')
print(raw_data_file_path_01)
raw_data_01 = np.genfromtxt(raw_data_file_path_01, delimiter=',')

print(raw_data_file_path_02)
raw_data_02 = np.genfromtxt(raw_data_file_path_02, delimiter=',')

print(raw_data_file_path_03)
raw_data_03 = np.genfromtxt(raw_data_file_path_03, delimiter=',')

###############################################################
# hardcoded indexes for the variables
################################################################
tempo = 0
id_plus_ideal = 1
iq_plus_ideal = 2
id_plus_meas = 3
iq_plus_meas = 4
id_mwt_ideal = 5
iq_mwt_ideal = 6
id_mwt_meas = 7
iq_mwt_meas = 8

##################################################
# the figure where the plots will be
##################################################
fig, axs = plt.subplots(2, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
fig.subplots_adjust(hspace=0.05, left=0.175, bottom=0.125, right=0.95, top=0.98)
linewidth = 0.75

start_time = 0
end_time = 0.08

##################################################
# plot 1 - direct
##################################################
axs[0].plot(raw_data_01[:, tempo],
            raw_data_01[:, id_mwt_ideal],color='black', linewidth=linewidth, linestyle=':', label=r'Ideal')
axs[0].plot(raw_data_01[:, tempo],
            raw_data_01[:, id_mwt_meas],color='red', linewidth=linewidth, linestyle='-', label=r'$\zeta=\sqrt{2}/2$')
axs[0].plot(raw_data_02[:, tempo],
            raw_data_02[:, id_mwt_meas],color='blue', linewidth=linewidth, linestyle='-', label=r'$\zeta/5$')
axs[0].plot(raw_data_03[:, tempo],
            raw_data_03[:, id_mwt_meas],color='green', linewidth=linewidth, linestyle='-', label=r'$\zeta/10$')
axs[0].set_xlim(start_time, end_time)
axs[0].legend(loc='upper right')

##################################################
# plot 2 - quadrature
##################################################
axs[1].plot(raw_data_01[:, tempo],
            raw_data_01[:, iq_mwt_ideal],color='black', linewidth=linewidth, linestyle=':', label=r'Ideal')
axs[1].plot(raw_data_01[:, tempo],
            raw_data_01[:, iq_mwt_meas],color='red', linewidth=linewidth, linestyle='-', label=r'$\zeta$')
axs[1].plot(raw_data_02[:, tempo],
            raw_data_02[:, iq_mwt_meas],color='blue', linewidth=linewidth, linestyle='-', label=r'$\zeta/5$')
axs[1].plot(raw_data_03[:, tempo],
            raw_data_03[:, iq_mwt_meas],color='green', linewidth=linewidth, linestyle='-', label=r'$\zeta/10$')
axs[1].set_xlim(start_time, end_time)
#axs[1].legend(loc='upper right')

axs[0].set_ylabel(r'Direct curr. $i_d$ (A)')
axs[1].set_ylabel(r'Quadrature curr. $i_q$ (A)')
axs[1].set_xlabel(r'Time (s)')

##################################################
# saving and showing
##################################################
fig.align_ylabels(axs[:])
print('Saving path and file:')
print(save_path)
plt.savefig(save_path, format='eps')
plt.show()
