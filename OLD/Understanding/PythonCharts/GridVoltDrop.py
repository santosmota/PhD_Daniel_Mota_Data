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

simulation_path = 'C:/Users/daniemot/OneDrive - NTNU/Publications/2021_PosNegSequences/matlab/Basics/'

caso = 'viabcpqui_Pos_notch'
#caso = 'viabcpqui_Neg_notch'

#caso = 'viabcpqui_Pos_lpf'
#caso = 'viabcpqui_Neg_lpf'

#caso = 'StepIq_notch'
#caso = 'StepIq_lpf'


start_time = 0.49
end_time = 0.65

raw_data_file_name = caso + '.txt'

raw_data_file_path = simulation_path + raw_data_file_name

save_path = simulation_path + picture_folder + caso + '.eps'

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
# plot 1 - grid voltage
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
#axs[0].set_xlim(start_time, end_time)
#axs[0].legend(loc='upper right')
axs[0].set_ylabel(r'$v_{g\,abc}$ (pu)')

##################################################
# plot 2 - Converter voltage
##################################################
axs[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vca],
            color='red', linewidth=linewidth, linestyle='-',label=r'$a$')
axs[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vcb],
            color='green', linewidth=linewidth, linestyle='-',label=r'$b$')
axs[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vcc],
            color='blue', linewidth=linewidth, linestyle='-',label=r'$c$')
axs[1].set_xlim(start_time, end_time)
#axs[1].legend(loc='upper right')
axs[1].set_ylabel(r'$v_{c\,abc}$ (pu)')

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
# plot 3 - Converter current
##################################################
axs[3].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, p],
            color='black', linewidth=linewidth, linestyle='-',label=r'$p$')
axs[3].set_xlim(start_time, end_time)
#axs[3].legend(loc='upper right')
axs[3].set_ylabel(r'Power (pu)')
axs[3].set_xlabel(r'Time (s)')
axs[3].set_xticks(np.arange(0.5, 0.650, 0.050))

##################################################
# saving and showing
##################################################
fig.align_ylabels(axs[:])
print('Saving path and file:')
print(save_path)
plt.savefig(save_path, format='eps')
plt.show()
