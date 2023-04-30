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
picture_folder = 'Notch/'

simulation_path = 'C:/Users/daniemot/OneDrive - NTNU/Publications/2021_PosNegSequences/matlab/Basics/'

start_freq = 25
end_freq = 175

raw_data_file_name = 'QualityFreqResp.txt'

raw_data_file_path = simulation_path + raw_data_file_name

save_path = simulation_path + picture_folder + 'QualityFreqResp.eps'

###############################################################
# reading data from csv files
################################################################
print('Opening files:')
print(raw_data_file_path)
raw_data = np.genfromtxt(raw_data_file_path, delimiter=',')

###############################################################
# hardcoded indexes for the variables
################################################################
w = 0
g1 = 1
g2 = 2
g3 = 3
g4 = 4
g5 = 5
f1 = 6
f2 = 7
f3 = 8
f4 = 9
f5 = 10

##################################################
# the figure where the plots will be
##################################################
fig, axs = plt.subplots(2, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
fig.subplots_adjust(hspace=0.075, left=0.175, bottom=0.175, right=0.95, top=0.98)
linewidth = 0.75

##################################################
# plot 0 - Gain
##################################################
axs[0].plot(raw_data[:, w],
            raw_data[:, g1],
            linewidth=linewidth, linestyle='-',label=r'$\zeta = 0.3$') #color='black'
axs[0].plot(raw_data[:, w],
            raw_data[:, g2],
            linewidth=linewidth, linestyle='-',label=r'$\zeta = 0.5$') #color='black'
axs[0].plot(raw_data[:, w],
            raw_data[:, g3],
            linewidth=linewidth, linestyle='-',label=r'$\zeta = 0.7$') #color='black'
axs[0].plot(raw_data[:, w],
            raw_data[:, g4],
            linewidth=linewidth, linestyle='-',label=r'$\zeta = 0.9$') #color='black'
#axs[0].set_xlim(start_freq, end_freq)
axs[0].set_ylim(0, 1)
axs[0].set_xticks(np.arange(-90, 120, 30))
axs[0].legend(loc='upper right')
axs[0].set_ylabel(r'Gain (pu)')

##################################################
# plot 1 - Phase
##################################################
axs[1].plot(raw_data[:, w],
            raw_data[:, f1],
            linewidth=linewidth, linestyle='-') #,label=r'$x_r$') #color='red'
axs[1].plot(raw_data[:, w],
            raw_data[:, f2],
            linewidth=linewidth, linestyle='-')
axs[1].plot(raw_data[:, w],
            raw_data[:, f3],
            linewidth=linewidth, linestyle='-')
axs[1].plot(raw_data[:, w],
            raw_data[:, f4],
            linewidth=linewidth, linestyle='-')
axs[1].set_xlim(start_freq, end_freq)
axs[1].set_ylim(-90, 90)
axs[1].set_yticks(np.arange(-90, 90, 45))
#axs[1].legend(loc='upper right')
axs[1].set_ylabel(r'Phase ($^\circ$)')
axs[1].set_xlabel(r'Frequency (Hz)')
axs[1].set_xticks(np.arange(start_freq, end_freq+25, 25))

##################################################
# saving and showing
##################################################
fig.align_ylabels(axs[:])
print('Saving path and file:')
print(save_path)
plt.savefig(save_path, format='eps')
plt.show()
