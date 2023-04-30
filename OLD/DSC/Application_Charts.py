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
figsizex = 6
figsizey = 4

###############################################################
# file path
###############################################################
picture_folder = 'GridVoltDrop/'

simulation_path = 'C:/Users/daniemot/OneDrive - NTNU/Publications/2021_COMPEL/DSCdq_COMPEL2021/'

#caso = 'Application_Unb'
caso = 'Application_Bal'

#detail = 1  # shorter time window if adjusted
detail = 1
namedetail = ''

if caso == 'Application_Unb':
    if detail == 1:
        start_time = 1.0 - 0.006
        end_time = 1.0 + 0.04
        namedetail = '_Detail'
    else:
        #start_time = 0.985
        #end_time = 1.095
        start_time = 0.9
        end_time = 1.4

else:
    if detail == 1:
        start_time = 1.0 - 0.006
        end_time = 1.0 + 0.04
        namedetail = '_Detail'
    else:
        #start_time = 0.985
        #end_time = 1.135
        start_time = 0.9
        end_time = 1.4

raw_data_file_name_ab = caso + '_DSCab.txt'
raw_data_file_name_dq = caso + '_DSCdq.txt'
raw_data_file_name_notch = caso + '_Notch.txt'

raw_data_file_path_ab = simulation_path + raw_data_file_name_ab
raw_data_file_path_dq = simulation_path + raw_data_file_name_dq
raw_data_file_path_notch = simulation_path + raw_data_file_name_notch

save_path = 'C:/Users/daniemot/OneDrive - NTNU/Publications/2021_COMPEL/Python/' + caso + namedetail + '.eps'

###############################################################
# reading data from csv files
################################################################
print('Opening file DSC ab:')
print(raw_data_file_path_ab)
raw_data_ab = np.genfromtxt(raw_data_file_path_ab, delimiter=',')

print('Opening file DSC dq:')
print(raw_data_file_path_dq)
raw_data_dq = np.genfromtxt(raw_data_file_path_dq, delimiter=',')

print('Opening file DSC notch:')
print(raw_data_file_path_notch)
raw_data_notch = np.genfromtxt(raw_data_file_path_notch, delimiter=',')

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
for aux in range(0, len(raw_data_ab[:, tempo]), 1):
    if start_time >= raw_data_ab[aux, tempo]:
        start_time_index = aux
    elif end_time >= raw_data_ab[aux, tempo]:
        end_time_index = aux

##################################################
# the figure where the plots will be
##################################################
fig, axs = plt.subplots(3, 2, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
#fig.subplots_adjust(hspace=0.075, left=0.175, bottom=0.125, right=0.95, top=0.98)
#fig.subplots_adjust(hspace=0.075, left=0.275, bottom=0.125, right=0.925, top=0.98)
#####fig.subplots_adjust(hspace=0.075, left=0.25, bottom=0.175, right=0.925, top=0.98)
linewidth = 0.75

##################################################
# plot 0 0 - freq
##################################################
axs[0][0].plot(raw_data_ab[start_time_index:end_time_index, tempo],
            raw_data_ab[start_time_index:end_time_index, f],
            color='black', linewidth=linewidth, linestyle='-',label=r'$f$')
#axs[0].set_xlim(start_time, end_time)
#axs[0][0].legend(frameon=False)
#axs[0][0].set_ylabel(r'$f$ (pu)')
axs[0][0].set_ylabel(r'Frequency (pu)')
if caso == 'Application_Unb':
    axs[0][0].legend(loc='lower left', frameon=False)
else:
    axs[0][0].legend(loc='lower right', frameon=False)

##################################################
# plot 1 0 - n
##################################################
axs[1][0].plot(raw_data_ab[start_time_index:end_time_index, tempo],
            raw_data_ab[start_time_index:end_time_index, n],
            color='black', linewidth=linewidth, linestyle='-', label=r'$n$')
#axs[0][0].set_xlim(start_time, end_time)
#axs[0][0].legend(loc='upper right')
#axs[1][0].set_ylabel(r'$n$')
axs[1][0].set_ylabel(r'DSC delay')
if caso == 'Application_Unb':
    axs[1][0].legend(loc='upper left', frameon=False)
else:
    axs[1][0].legend(loc='upper right', frameon=False)


##################################################
# plot 2 0 - grid voltage
##################################################
axs[2][0].plot(raw_data_ab[start_time_index:end_time_index, tempo],
            raw_data_ab[start_time_index:end_time_index, vga],
            color='magenta', linewidth=linewidth, linestyle='-', label=r'$a$')
axs[2][0].plot(raw_data_ab[start_time_index:end_time_index, tempo],
            raw_data_ab[start_time_index:end_time_index, vgb],
            color='green', linewidth=linewidth, linestyle='-', label=r'$b$')
axs[2][0].plot(raw_data_ab[start_time_index:end_time_index, tempo],
            raw_data_ab[start_time_index:end_time_index, vgc],
            color='blue', linewidth=linewidth, linestyle='-', label=r'$c$')
#axs[2][0].legend(loc='lower right')
#axs[2][0].set_ylabel(r'$v_{abc}$ (pu)')
axs[2][0].set_ylabel(r'Grid voltage (pu)')
axs[2][0].set_xlim(start_time, end_time)
axs[2][0].set_xlabel(r'Time (s)')

##################################################
# plot 3 - active power
##################################################
axs[0][1].plot(raw_data_notch[start_time_index:end_time_index, tempo],
            raw_data_notch[start_time_index:end_time_index, p],
            color='red', linewidth=linewidth, linestyle='-', label=r'Notch')
axs[0][1].plot(raw_data_ab[start_time_index:end_time_index, tempo],
            raw_data_ab[start_time_index:end_time_index, p],
            color='black', linewidth=linewidth, linestyle='-.', label=r'DSC$_{\alpha \beta}$')
axs[0][1].plot(raw_data_ab[start_time_index:end_time_index, tempo],
            raw_data_ab[start_time_index:end_time_index, p],
            color='black', linewidth=linewidth, linestyle=':', label=r'DSC$_{dq}$')
#axs[0][1].set_ylabel(r'$p$ (pu)')
axs[0][1].set_ylabel(r'Act.power (pu)')
#if caso == 'Application_Unb':
#   axs[0][1].legend(loc='upper right', frameon=False)
#else:
#    axs[0][1].legend(loc='center right', frameon=False)

##################################################
# plot - reactive power
##################################################
axs[1][1].plot(raw_data_notch[start_time_index:end_time_index, tempo],
            raw_data_notch[start_time_index:end_time_index, q],
            color='red', linewidth=linewidth, linestyle='-', label=r'Notch')
axs[1][1].plot(raw_data_ab[start_time_index:end_time_index, tempo],
            raw_data_ab[start_time_index:end_time_index, q],
            color='black', linewidth=linewidth, linestyle='-.', label=r'DSC$_{\alpha \beta}$')
axs[1][1].plot(raw_data_ab[start_time_index:end_time_index, tempo],
            raw_data_ab[start_time_index:end_time_index, q],
            color='black', linewidth=linewidth, linestyle=':', label=r'DSC$_{dq}$')
#axs[1][1].legend(loc='upper right')
#axs[1][1].set_ylabel(r'$q$ (pu)')
axs[1][1].set_ylabel(r'React.power (pu)')
if caso == 'Application_Bal':
    axs[1][1].legend(loc='lower right', frameon=False)


##################################################
# plot - dc voltage
##################################################
axs[2][1].plot(raw_data_notch[start_time_index:end_time_index, tempo],
            raw_data_notch[start_time_index:end_time_index, vdc],
            color='red', linewidth=linewidth, linestyle='-', label=r'Notch')
axs[2][1].plot(raw_data_ab[start_time_index:end_time_index, tempo],
            raw_data_ab[start_time_index:end_time_index, vdc],
            color='black', linewidth=linewidth, linestyle='-.', label=r'DSC$_{\alpha \beta}$')
axs[2][1].plot(raw_data_ab[start_time_index:end_time_index, tempo],
            raw_data_ab[start_time_index:end_time_index, vdc],
            color='black', linewidth=linewidth, linestyle=':', label=r'DSC$_{dq}$')
#axs[1][1].legend(loc='upper right')
#axs[2][1].set_ylabel(r'$v_{dc}$ (pu)')
axs[2][1].set_ylabel(r'dc voltage (pu)')
axs[2][1].set_xlabel(r'Time (s)')

if caso == 'Application_Unb':
    axs[2][1].legend(loc='center right', frameon=False)
#else:
#    axs[2][1].legend(loc='center right', frameon=False)

if detail == 0:
    axs[2][1].set_xticks(np.arange(0, 2, 0.1))
else:
    axs[2][1].set_xticks(np.arange(0, 2, 0.01))

axs[2][1].set_xlim(start_time, end_time)

fig.tight_layout()


##################################################
# saving and showing
##################################################
fig.align_ylabels(axs[:])
print('Saving path and file:')
print(save_path)
plt.savefig(save_path, format='eps')
plt.show()
