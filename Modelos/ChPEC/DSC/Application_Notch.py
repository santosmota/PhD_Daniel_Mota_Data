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
figsizex = 3 #5
figsizey = 3.5

###############################################################
# file path
###############################################################
picture_folder = 'GridVoltDrop/'

simulation_path = 'C:/Users/daniemot/OneDrive - NTNU/Publications/2022_ISGT_NA/Matlab/'

#caso = 'Application_Unb_Notch'
#caso = 'Application_Bal_Notch'

#start_time = 0.98
#end_time = 1.105

start_time = 0.99
end_time = 1.055

raw_data_file_name = caso + '.txt'

raw_data_file_path = simulation_path + raw_data_file_name

save_path = 'C:/Users/daniemot/OneDrive - NTNU/Publications/2022_ISGT_NA/Python/' + caso + '.eps'

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
ia = 4
ib = 5
ic = 6
f = 7
p = 8
q = 9
vdc = 10
n = 11

###############################################################
# finding the indexes for the time  (lazy programming)
################################################################
for aux in range(0, len(raw_data[:, tempo]), 1):
    if start_time >= raw_data[aux, tempo]:
        start_time_index = aux
    elif end_time >= raw_data[aux, tempo]:
        end_time_index = aux

##################################################
# the figure where the plots will be
##################################################
fig, axs = plt.subplots(4, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
#fig.subplots_adjust(hspace=0.075, left=0.175, bottom=0.125, right=0.95, top=0.98)
fig.subplots_adjust(hspace=0.075, left=0.275, bottom=0.125, right=0.925, top=0.98)
#####fig.subplots_adjust(hspace=0.075, left=0.25, bottom=0.175, right=0.925, top=0.98)
linewidth = 0.75

##################################################
# plot 0 - freq
##################################################
axs[0].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, f],
            color='black', linewidth=linewidth, linestyle='-',label=r'$f$')
#axs[0].set_xlim(start_time, end_time)
#axs[0].legend(loc='upper right')
axs[0].set_ylabel(r'$f$ (pu)')

##################################################
# plot 1 - grid voltage
##################################################
axs[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vga],
            color='red', linewidth=linewidth, linestyle='-',label=r'$a$')
axs[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vgb],
            color='green', linewidth=linewidth, linestyle='-',label=r'$b$')
axs[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vgc],
            color='blue', linewidth=linewidth, linestyle='-',label=r'$c$')
#axs[0].set_xlim(start_time, end_time)
#axs[0].legend(loc='upper right')
axs[1].set_ylabel(r'$v_{abc}$ (pu)')

##################################################
# plot 3 - Converter current
##################################################
axs[2].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, ia],
            color='red', linewidth=linewidth, linestyle='-',label=r'$a$')
axs[2].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, ib],
            color='green', linewidth=linewidth, linestyle='-',label=r'$b$')
axs[2].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, ic],
            color='blue', linewidth=linewidth, linestyle='-',label=r'$c$')
axs[2].set_xlim(start_time, end_time)
#axs[2].legend(loc='upper right')
axs[2].set_ylabel(r'$i_{abc}$ (pu)')

##################################################
# plot 4 - vdc
##################################################
axs[3].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vdc],
            color='magenta', linewidth=linewidth, linestyle='-', label=r'$v_{dc}$')
axs[3].set_xlim(start_time, end_time)
axs[3].set_ylim(0.975, 1.025)
#axs[3].legend(loc='upper right')
axs[3].set_ylabel(r'$v_{dc}$ (pu)')
axs[3].set_xlabel(r'Time (s)')
#axs[3].set_xticks(np.arange(0.5, 0.650, 0.050))

##################################################
# saving and showing
##################################################
fig.align_ylabels(axs[:])
print('Saving path and file:')
print(save_path)
#plt.savefig(save_path, format='eps')
plt.show()
