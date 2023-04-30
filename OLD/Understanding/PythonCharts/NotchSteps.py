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
figsizey = 1.5

###############################################################
# file path
###############################################################
picture_folder = 'Notch/'

simulation_path = 'C:/Users/daniemot/OneDrive - NTNU/Publications/2021_PosNegSequences/matlab/Basics/'

start_time = 0
end_time = 0.025

raw_data_file_name = 'QualitySteps.txt'

raw_data_file_path = simulation_path + raw_data_file_name

save_path = simulation_path + picture_folder + 'QualitySteps.eps'

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
s1 = 1
s2 = 2
s3 = 3
s4 = 4
s5 = 5

##################################################
# the figure where the plots will be
##################################################
fig, axs = plt.subplots(1, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
fig.subplots_adjust(hspace=0.075, left=0.175, bottom=0.275, right=0.95, top=0.98)
linewidth = 0.75

##################################################
# plot 0 - Gain
##################################################
axs.plot(raw_data[:, w],
            raw_data[:, s1],
            linewidth=linewidth, linestyle='-',label=r'$\zeta = 0.3$') #color='black'
axs.plot(raw_data[:, w],
            raw_data[:, s2],
            linewidth=linewidth, linestyle='-',label=r'$\zeta = 0.5$') #color='black'
axs.plot(raw_data[:, w],
            raw_data[:, s3],
            linewidth=linewidth, linestyle='-',label=r'$\zeta = 0.7$') #color='black'
axs.plot(raw_data[:, w],
            raw_data[:, s4],
            linewidth=linewidth, linestyle='-',label=r'$\zeta = 0.9$') #color='black'
axs.set_xlim(start_time, end_time)
axs.set_ylim(0.2, 1.2)
#axs[0].set_xticks(np.arange(-90, 120, 30))
axs.legend(loc='lower right')
axs.set_ylabel(r'Amplitude (pu)')
#axs.set_yticks(np.arange(-90, 90, 45))
axs.set_xlabel(r'Time (s)')
#axs[0].set_xticks(np.arange(start_time, end_time + 25, 25))

##################################################
# saving and showing
##################################################
#fig.align_ylabels(axs[:])
print('Saving path and file:')
print(save_path)
plt.savefig(save_path, format='eps')
plt.show()
