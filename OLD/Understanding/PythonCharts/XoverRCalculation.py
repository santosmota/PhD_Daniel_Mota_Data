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
picture_folder = 'XoverRCalculation/'

simulation_path = 'C:/Users/daniemot/OneDrive - NTNU/Publications/2021_PosNegSequences/matlab/Basics/'

start_freq = 2500
end_freq = 4000

raw_data_file_name = 'XoverRCalculation.txt'

raw_data_file_path = simulation_path + raw_data_file_name

save_path = simulation_path + picture_folder + 'XoverRCalculation.eps'

###############################################################
# reading data from csv files
################################################################
print('Opening files:')
print(raw_data_file_path)
raw_data = np.genfromtxt(raw_data_file_path, delimiter=',')

###############################################################
# hardcoded indexes for the variables
################################################################
fsw = 0
fres = 1
rc = 2
xr = 3
xoverr = 4

##################################################
# the figure where the plots will be
##################################################
fig, axs = plt.subplots(3, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
fig.subplots_adjust(hspace=0.075, left=0.175, bottom=0.175, right=0.95, top=0.98)
linewidth = 0.75

##################################################
# plot 0 - X over R
##################################################
axs[0].plot(raw_data[:, fsw],
            raw_data[:, xoverr],
            color='black', linewidth=linewidth, linestyle='-',label=r'$X/R$')
#axs[0].set_xlim(start_freq, end_freq)
axs[0].legend(loc='upper right')
axs[0].set_ylabel(r'$X/R$ (pu)')

##################################################
# plot 1 - Reactance and resistance
##################################################
axs[1].plot(raw_data[:, fsw],
            raw_data[:, xr],
            color='red', linewidth=linewidth, linestyle='-',label=r'$x_r$')
axs[1].plot(raw_data[:, fsw],
            raw_data[:, rc],
            color='blue', linewidth=linewidth, linestyle='-',label=r'$r_c$')
#axs[0].set_xlim(start_freq, end_freq)
axs[1].legend(loc='upper right')
axs[1].set_ylabel(r'Imp. ($\Omega$)')

##################################################
# plot 2 - Resonance frequency
##################################################
axs[2].plot(raw_data[:, fsw],
            raw_data[:, fres],
            color='green', linewidth=linewidth, linestyle='-',label=r'$f_{res}$')
axs[2].set_xlim(start_freq, end_freq)
axs[2].legend(loc='lower right')
axs[2].set_ylabel(r'$f_{res}$ (Hz)')
axs[2].set_xlabel(r'Switching frequency (Hz)')
axs[2].set_xticks(np.arange(start_freq, end_freq+250, 250))

##################################################
# saving and showing
##################################################
fig.align_ylabels(axs[:])
print('Saving path and file:')
print(save_path)
plt.savefig(save_path, format='eps')
plt.show()
