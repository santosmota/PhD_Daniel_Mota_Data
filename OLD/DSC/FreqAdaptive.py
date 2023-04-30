#FFTs of several measuring principles

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
# file path
###############################################################
picture_folder = 'C:/Users/daniemot/OneDrive - NTNU/Publications/2021_PELS_Letter_DSCdq/Latex/Figures/'

matlab_path = 'C:/Users/daniemot/OneDrive - NTNU/Publications/2021_PELS_Letter_DSCdq/Matlab/'

raw_dados_file_name = 'FreqAdaptive_Raw'
raw_dados_full_file_path = matlab_path + raw_dados_file_name + '.txt'

save_file_name = 'FreqAdaptive'
save_full_file_path = picture_folder + save_file_name + '.eps'

###############################################################
# reading raw dados from csv files
################################################################
print('Opening raw dados file:')
print(raw_dados_full_file_path)
dados = np.genfromtxt(raw_dados_full_file_path, delimiter=',')

###############################################################
# hardcoded indexes for the variables
################################################################
time = 0
vd = 1
vq = 2
vd_r = 3
vq_r = 4
vd_c = 5
vq_c = 6
vd_f = 7
vq_f = 8
vd_w = 9
vq_w = 10
f = 11
n = 12
va = 13
vb = 14
vc = 15

###############################################################
# size of the figure
###############################################################
figsizex = 5
figsizey = 4

##################################################
# the figure where the plots will be
##################################################
fig, axs = plt.subplots(3, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
fig.subplots_adjust(hspace=0.075, left=0.175, bottom=0.125, right=0.95, top=0.98)
linewidth = 0.75

#dados[:, time] = 1000 * dados[:, time]
start_time = 0
end_time = 0.25

start_time_index = 0
end_time_index = None

#lightcolor = (0.7, 0.7, 0.7)

##################################################
# subplot on top - Inverter voltages
##################################################
axs[0].plot(dados[start_time_index:end_time_index, time],
            dados[start_time_index:end_time_index, va],
            color='red', linewidth=linewidth, linestyle='-', label=r'$v_a$')
axs[0].plot(dados[start_time_index:end_time_index, time],
            dados[start_time_index:end_time_index, vb],
            color='blue', linewidth=linewidth, linestyle='-', label=r'$v_b$')
axs[0].plot(dados[start_time_index:end_time_index, time],
            dados[start_time_index:end_time_index, vc],
            color='green', linewidth=linewidth, linestyle='-', label=r'$v_c$')

##################################################
# Number
#axs[1].plot(dados[start_time_index:end_time_index, time],
#            dados[start_time_index:end_time_index, vd_notch],
#            color='green', linewidth=linewidth, linestyle='-', label=r'Notch')
axs[1].plot(np.array([0, 0.25]),
            np.array([75, 75]),
            color='red', linewidth=linewidth, linestyle='-', label=r'$n_c$')

axs[1].plot(dados[start_time_index:end_time_index, time],
            dados[start_time_index:end_time_index, n],
            color='black', linewidth=linewidth, linestyle='-', label=r'$n$')

axs[1].plot(np.array([0, 0.25]),
            np.array([74, 74]),
            color='blue', linewidth=linewidth, linestyle='-', label=r'$n_f$')



##################################################
# Direct axis
axs[2].plot(dados[start_time_index:end_time_index, time],
            dados[start_time_index:end_time_index, vd_c],
            color='red', linewidth=linewidth, linestyle='-', label=r'$v_{d+c}$')

axs[2].plot(dados[start_time_index:end_time_index, time],
            dados[start_time_index:end_time_index, vd_w],
            color='green', linewidth=linewidth, linestyle='-', label=r'$v_{d+w}$')

axs[2].plot(dados[start_time_index:end_time_index, time],
            dados[start_time_index:end_time_index, vd_f],
            color='blue', linewidth=linewidth, linestyle='-', label=r'$v_{d+f}$')



##################################################
# Legends and titles
axs[0].set_xlim(start_time, end_time)
axs[0].set_ylabel(r'Volt. $abc$ (pu)')

axs[0].legend(loc='center right')
axs[1].legend(loc='lower right')
axs[2].legend(loc='lower right')

axs[1].set_ylabel(r'Delayed samples')
axs[2].set_ylabel(r'Direct axis (pu)')
axs[2].set_xlabel(r'Time (s)')

#axs[2].set_yticks(np.arange(0, 1, 0.025))
axs[2].set_ylim(0.997, 1.003)


##################################################
# saving and showing
##################################################
fig.align_ylabels(axs[:])
print('Saving path and file:')
print(save_full_file_path)
plt.savefig(save_full_file_path, format='eps')
plt.show()