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

raw_dados_file_name = 'FreqAdaptiveFFT_Raw'
raw_dados_full_file_path = matlab_path + raw_dados_file_name + '.txt'

save_file_name = 'FreqAdaptiveFFT'
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
ind_time = 0
ind_x = 1
ind_yc = 2
ind_yf = 3
ind_yw = 4

###############################################################
# adding zeros to increase FFTs resolution
################################################################
deltat = dados[1, ind_time] - dados[0, ind_time]
Fs = 1/deltat
FFTres = 0.01
Janela = 1/FFTres
Nsamp = int(Janela / deltat)
Nsamp2 = int(Nsamp/2)

x = np.zeros(Nsamp)
yc = np.zeros(Nsamp)
yf = np.zeros(Nsamp)
yw = np.zeros(Nsamp)

freq = np.fft.fftfreq(x.shape[-1])
freq = Fs*freq[1:Nsamp2]

for cnt in range(0, len(dados[:, ind_time])):
    x[cnt] = dados[cnt, ind_x]
    yc[cnt] = dados[cnt, ind_yc]
    yf[cnt] = dados[cnt, ind_yf]
    yw[cnt] = dados[cnt, ind_yw]

##################################################
# the figure where the Gain will be
##################################################
figsizex = 5
figsizey = 2.5
largura = 0.75

figSysID, axsSysID = plt.subplots(2, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
figSysID.subplots_adjust(hspace=0.075, left=0.175, bottom=0.175, right=0.95, top=0.98)

start_freq = 118
end_freq = 124

#start_freq = 0
#end_freq = 140


#lightcolor = (0.7, 0.7, 0.7)

##################################################
# subplot on top
##################################################

fft_x = np.fft.fft(x)
fft_x = 2 * fft_x[1:Nsamp2]/Nsamp

fft_y = np.fft.fft(yc)
fft_y = 2 * fft_y[1:Nsamp2]/Nsamp
axsSysID[0].plot(freq, np.absolute(np.divide(fft_y, fft_x)), color='r', linewidth=largura, linestyle='-', label=r'$n_c=75$')
axsSysID[1].plot(freq, 180 / np.pi * np.angle(np.divide(fft_y, fft_x)), color='r', linewidth=largura, linestyle='-', label=r'$n_c=75$')

fft_y = np.fft.fft(yf)
fft_y = 2 * fft_y[1:Nsamp2]/Nsamp
axsSysID[0].plot(freq, np.absolute(np.divide(fft_y, fft_x)), color='b', linewidth=largura, linestyle='-', label=r'$n_f=74$')
axsSysID[1].plot(freq, 180 / np.pi * np.angle(np.divide(fft_y, fft_x)), color='b', linewidth=largura, linestyle='-', label=r'$n_f=74$')

#fft_y = np.fft.fft(yw)
#fft_y = 2 * fft_y[1:Nsamp2]/Nsamp
#axsSysID[0].plot(freq, np.absolute(np.divide(fft_y, fft_x)), color='c', linewidth=largura, linestyle='-', label=r'weighted')
#axsSysID[1].plot(freq, 180 / np.pi * np.angle(np.divide(fft_y, fft_x)), color='c', linewidth=largura, linestyle='-', label=r'weighted')

axsSysID[1].set_xticks(np.arange(100, 200, 1))
axsSysID[1].set_xlim(start_freq, end_freq)

axsSysID[0].set_yticks(np.arange(0, 1, 0.025))
axsSysID[0].set_ylim(-0.005, 0.055)

axsSysID[0].set_ylabel(r'Gain (pu/pu)')
axsSysID[1].set_ylabel(r'Phase ($^\circ$)')

axsSysID[1].set_yticks(np.arange(-360,360,45))
axsSysID[1].set_ylim(-100, 100)

#axsSysID[1].set_yticks(np.arange(-360,360,2))
#axsSysID[1].set_ylim(-94, -86)

axsSysID[1].set_xlabel(r'Frequency (Hz)')
axsSysID[1].legend(loc='center right')

figSysID.align_ylabels(axsSysID[:])

print('Saving path and file:')
print(save_full_file_path)
#figSysID.savefig(save_full_file_path, format='eps')
plt.show()