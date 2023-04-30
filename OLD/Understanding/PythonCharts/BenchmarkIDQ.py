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
figsizex = 2.75
figsizey = 2.5

###############################################################
# file path
###############################################################
picture_folder = 'Comparison/'

simulation_path = 'C:/Users/daniemot/OneDrive - NTNU/Publications/2021_PosNegSequences/matlab/Basics/'

#raw_data_file_name = 'BenchPositive'
raw_data_file_name = 'BenchNegative'

raw_data_file_path = simulation_path + raw_data_file_name + '.txt'

save_path = simulation_path + picture_folder + raw_data_file_name + 'I.eps'


###############################################################
# reading data from csv files
################################################################
print('Opening files:')
print(raw_data_file_path)
raw_data = np.genfromtxt(raw_data_file_path, delimiter=',')

###############################################################
# hardcoded indexes for the variables
################################################################
tempo = 0
id_ideal = 1
iq_ideal = 2
id_notch = 3
iq_notch = 4
id_lpf = 5
iq_lpf = 6
id_ama = 7
iq_ama = 8

##################################################
# the figure where the plots will be
##################################################
fig, axs = plt.subplots(2, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
#fig.subplots_adjust(hspace=0.075, left=0.175, bottom=0.175, right=0.95, top=0.98)
fig.subplots_adjust(hspace=0.075, left=0.25, bottom=0.175, right=0.925, top=0.98)
linewidth = 0.75

start_time = 0
end_time = 0.06

##################################################
# plot 1 - direct
##################################################
axs[0].plot(raw_data[:, tempo],
            raw_data[:, id_ideal], color='black', linewidth=linewidth, linestyle='--', label=r'Ideal')
axs[0].plot(raw_data[:, tempo],
            raw_data[:, id_notch], color='red', linewidth=linewidth, linestyle='-', label=r'Notch')
axs[0].plot(raw_data[:, tempo],
            raw_data[:, id_lpf], color='blue', linewidth=linewidth, linestyle='-', label=r'LPF')
axs[0].set_xlim(start_time, end_time)
#axs[0].legend(loc='upper right')
axs[0].set_ylabel(r'Direct $i_d$ (pu)')


##################################################
# plot 2 - quadrature
##################################################
axs[1].plot(raw_data[:, tempo],
            raw_data[:, iq_ideal], color='black', linewidth=linewidth, linestyle='--', label=r'Ideal')
axs[1].plot(raw_data[:, tempo],
            raw_data[:, iq_notch], color='red', linewidth=linewidth, linestyle='-', label=r'Notch')
axs[1].plot(raw_data[:, tempo],
            raw_data[:, iq_lpf], color='blue', linewidth=linewidth, linestyle='-', label=r'LPF')
axs[1].set_xlim(start_time, end_time)
#axs[1].legend(loc='upper right')

axs[1].set_ylabel(r'Quadrat. $i_q$ (pu)')
axs[1].set_xlabel(r'Time (s)')

##################################################
# saving and showing
##################################################
fig.align_ylabels(axs[:])
print('Saving path and file:')
print(save_path)
plt.savefig(save_path, format='eps')
plt.show()
