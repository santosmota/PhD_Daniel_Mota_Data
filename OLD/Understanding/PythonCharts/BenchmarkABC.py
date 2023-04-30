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
figsizey = 2.5

###############################################################
# file path
###############################################################
picture_folder = 'Comparison/'

simulation_path = 'C:/Users/daniemot/OneDrive - NTNU/Publications/2021_PosNegSequences/matlab/Basics/'

raw_data_file_name = 'viabcpqui'

raw_data_file_path = simulation_path + raw_data_file_name + '.txt'

save_path = simulation_path + picture_folder + raw_data_file_name + '.eps'


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
vga = 1
vgb = 2
vgc = 3
vca = 4
vcb = 5
vcc = 6
ia = 7
ib = 8
ic = 9
p = 10
q = 11
v = 12
i = 13

##################################################
# the figure where the plots will be
##################################################
fig, axs = plt.subplots(2, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
fig.subplots_adjust(hspace=0.075, left=0.175, bottom=0.175, right=0.95, top=0.98)
linewidth = 0.75

start_time = 0
end_time = 0.14

start_time_index = 0
end_time_index = -1

##################################################
# plot 1 - Voltages
##################################################
axs[0].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vga],
            color='red', linewidth=linewidth, linestyle='-',label=r'$a$')
axs[0].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vgb],
            color='green', linewidth=linewidth, linestyle='-',label=r'$b$')
axs[0].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vgc],
            color='blue', linewidth=linewidth, linestyle='-',label=r'$c$')
axs[0].set_xlim(start_time, end_time)
axs[0].legend(loc='upper right')
axs[0].set_ylabel(r'Voltage (V)')


##################################################
# plot 2 - Currents
##################################################
axs[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, ia],
            color='red', linewidth=linewidth, linestyle='-',label=r'$a$')
axs[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, ib],
            color='green', linewidth=linewidth, linestyle='-',label=r'$b$')
axs[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, ic],
            color='blue', linewidth=linewidth, linestyle='-',label=r'$c$')
axs[1].set_xlim(start_time, end_time)
#axs[1].legend(loc='upper right')
axs[1].set_ylabel(r'Current (A)')
axs[1].set_xlabel(r'Time (s)')

##################################################
# saving and showing
##################################################
fig.align_ylabels(axs[:])
print('Saving path and file:')
print(save_path)
plt.savefig(save_path, format='eps')
plt.show()
