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

raw_data_file_name = 'ShortPulse_Raw'
raw_data_full_file_path = matlab_path + raw_data_file_name + '.txt'

save_file_name = 'ShortPulse_TimeDomain'
save_full_file_path = picture_folder + save_file_name + '.eps'

save_file_name = 'ShortPulse_FreqDomain'
save_full_file_path_SysId = picture_folder + save_file_name + '.eps'

###############################################################
# reading raw data from csv files
################################################################
print('Opening raw data file:')
print(raw_data_full_file_path)
dados = np.genfromtxt(raw_data_full_file_path, delimiter=',')

###############################################################
# hardcoded indexes for the variables
################################################################
time = 0
vd = 1
vq = 2
vd_notch = 3
vq_notch = 4
vd_DSC = 5
vq_DSC = 6
va = 7
vb = 8
vc = 9

delta_t = dados[1, time] - dados[0, time]
Nsamp = len(dados[:, time])

###############################################################
# size of the figure
###############################################################
figsizex = 5
#figsizey = 1.75
figsizey = 2.5

largura = 0.75

###############################################################
# FFT basics
###############################################################
Fs = 1/delta_t
Nsamp2 = int(Nsamp/2)
freq = np.fft.fftfreq(dados[:, time].shape[-1])
freq = Fs*freq[1:Nsamp2]

##################################################
# Figure for the time domain
##################################################
fig, axs = plt.subplots(2, 1, sharex=True, figsize=(figsizex, figsizey))
fig.subplots_adjust(hspace=0.075, left=0.175, bottom=0.175, right=0.95, top=0.98)

start_time = 0
end_time = 13

tempo = 1000 * dados[:, time]

axs[0].plot(tempo, dados[:, va], color='red', linewidth=largura, linestyle='-', label=r'$v_a$')
axs[0].plot(tempo, dados[:, vb], color='blue', linewidth=largura, linestyle='-', label=r'$v_b$')
axs[0].plot(tempo, dados[:, vc], color='green', linewidth=largura, linestyle='-', label=r'$v_c$')

axs[1].plot(tempo, dados[:, vd], color='black', linewidth=largura, linestyle='--', label=r'Ideal')
axs[1].plot(tempo, dados[:, vd_notch], color='red', linewidth=largura, linestyle='-', label=r'Notch')
axs[1].plot(tempo, dados[:, vd_DSC], color='blue', linewidth=largura, linestyle='-', label=r'DSC$_{\alpha \beta}$')

axs[0].set_ylabel(r'Volt. $abc$ (pu)')
axs[0].legend(loc='center right')

axs[1].set_xlim(start_time, end_time)
axs[1].set_ylabel(r'Direct axis (pu)')
axs[1].set_xlabel(r'Time (ms)')
axs[1].legend(loc='center right')

##################################################
# the figure where the Gain will be
##################################################
figsizex = 5
figsizey = 2.5
figSysID, axsSysID = plt.subplots(2, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
figSysID.subplots_adjust(hspace=0.075, left=0.175, bottom=0.175, right=0.95, top=0.98)

start_freq = 0
end_freq = 480

#lightcolor = (0.7, 0.7, 0.7)

##################################################
# subplot on top
##################################################

fft_dist = np.fft.fft(dados[:, vd])
fft_dist = 2 * fft_dist[1:Nsamp2]/Nsamp

fft_sig = np.fft.fft(dados[:, vd_notch])
fft_sig = 2 * fft_sig[1:Nsamp2]/Nsamp
axsSysID[0].plot(freq, np.absolute(np.divide(fft_sig, fft_dist)), color='r', linewidth=largura, linestyle='-', label=r'Notch')
axsSysID[1].plot(freq, 180 / np.pi * np.angle(np.divide(fft_sig, fft_dist)), color='r', linewidth=largura, linestyle='-', label=r'Notch')

fft_sig = np.fft.fft(dados[:, vd_DSC])
fft_sig = 2 * fft_sig[1:Nsamp2]/Nsamp
axsSysID[0].plot(freq, np.absolute(np.divide(fft_sig, fft_dist)), color='b', linewidth=largura, linestyle='-', label=r'DSC$_{\alpha \beta}$')
axsSysID[1].plot(freq, 180 / np.pi * np.angle(np.divide(fft_sig, fft_dist)), color='b', linewidth=largura, linestyle='-', label=r'DSC$_{\alpha \beta}$')

axsSysID[1].set_xticks(np.arange(0, 1200, 60))
axsSysID[1].set_xlim(start_freq, end_freq)

axsSysID[0].set_ylabel(r'Gain (pu/pu)')
axsSysID[1].set_ylabel(r'Phase ($^\circ$)')

axsSysID[1].set_yticks(np.arange(-360,360,45))
#axsSysID[1].set_ylim(-180, 100)
axsSysID[1].set_ylim(-100, 100)
axsSysID[1].set_xlabel(r'Frequency (Hz)')
#axsSysID[0].legend(loc='lower right')
axsSysID[1].legend(loc='lower right')

figSysID.align_ylabels(axsSysID[:])

print('Saving path and file:')
print(save_full_file_path)
#fig.savefig(save_full_file_path, format='eps')
#figSysID.savefig(save_full_file_path_SysId, format='eps')
plt.show()