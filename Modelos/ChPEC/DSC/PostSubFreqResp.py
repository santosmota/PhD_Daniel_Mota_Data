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
figsizey = 4

###############################################################
# file path
###############################################################
picture_folder = 'Comparison/'

simulation_path = 'C:/Users/daniemot/OneDrive - NTNU/Publications/2021_PosNegSequences/matlab/Basics/'

raw_data_file_name = 'PostSubmFreqResp'

raw_data_file_path = simulation_path + raw_data_file_name + '.txt'

save_path_1 = simulation_path + picture_folder + raw_data_file_name + '_time.eps'
save_path_2 = simulation_path + picture_folder + raw_data_file_name + '_freq.eps'


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
amp = 1
va = 2
vb = 3
vc = 4
ia = 5
ib = 6
ic = 7
vd_notch = 8
vq_notch = 9
id_notch = 10
iq_notch = 11
vd_lpf = 12
vq_lpf = 13
id_lpf = 14
iq_lpf = 15
vd = 16
vq = 17
id = 18
iq = 19


##################################################
##################################################
##################################################
# Voltages no tempo
##################################################
# the figure where the plots will be
##################################################
fig, axs = plt.subplots(3, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
fig.subplots_adjust(hspace=0.075, left=0.175, bottom=0.125, right=0.95, top=0.98)
linewidth = 0.75

start_time = 0
end_time = 0.02

start_time_index = 0
end_time_index = 0
while raw_data[end_time_index, tempo] < end_time:
    end_time_index = end_time_index + 1

##################################################
# plot 1 - Voltages abc
##################################################
axs[0].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, va],
            color='red', linewidth=linewidth, linestyle='-',label=r'$v_a$')
axs[0].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vb],
            color='green', linewidth=linewidth, linestyle='-',label=r'$v_b$')
axs[0].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vc],
            color='blue', linewidth=linewidth, linestyle='-',label=r'$v_c$')
axs[0].set_xlim(start_time, end_time)
axs[0].legend(loc='upper right')
axs[0].set_ylabel(r'Volt. (pu)')
#################################################
# plot 2 - Notch
##################################################
axs[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vd],
            color='black', linewidth=linewidth, linestyle=':',label=r'$v_{d+}$ ideal')
#axs[1].plot(raw_data[start_time_index:end_time_index, tempo],
#            raw_data[start_time_index:end_time_index, vq],
#            color='blue', linewidth=linewidth, linestyle=':',label=r'$q$')
axs[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vd_notch],
            color='red', linewidth=linewidth, linestyle='-',label=r'$v_{d+}$ notch')
#axs[1].plot(raw_data[start_time_index:end_time_index, tempo],
#            raw_data[start_time_index:end_time_index, vq_notch],
#            color='blue', linewidth=linewidth, linestyle='-',label=r'$q+$')
axs[1].set_xlim(start_time, end_time)
axs[1].legend(loc='upper right')
axs[1].set_ylabel(r'Notch (pu)')
#################################################
# plot 3 - LPF
##################################################
axs[2].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vd],
            color='black', linewidth=linewidth, linestyle=':',label=r'$v_{d+}$ ideal')
#axs[2].plot(raw_data[start_time_index:end_time_index, tempo],
#            raw_data[start_time_index:end_time_index, vq],
#            color='blue', linewidth=linewidth, linestyle=':',label=r'$q$')
axs[2].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, vd_lpf],
            color='blue', linewidth=linewidth, linestyle='-', label=r'$v_{d+}$ LPF')
#axs[2].plot(raw_data[start_time_index:end_time_index, tempo],
#            raw_data[start_time_index:end_time_index, vq_lpf],
#            color='blue', linewidth=linewidth, linestyle='-', label=r'$q+$')
axs[2].set_xlim(start_time, end_time)
axs[2].legend(loc='upper right')
axs[2].set_ylabel(r'LPF (pu)')
axs[2].set_xlabel(r'Time (s)')


##################################################
# saving and showing
##################################################
fig.align_ylabels(axs[:])
print('Saving path and file:')
print(save_path_1)
#plt.savefig(save_path, format='eps')
#plt.show()

###############################################################
# FFT basics
###############################################################

Ts = raw_data[1, tempo] - raw_data[0, tempo]
Ttot = raw_data[None, tempo]
Fs = 1/Ts
Nsamp = len(raw_data[:, tempo])
#Nsamp2 = int(Nsamp/2)

freq = Fs * np.fft.fftfreq(raw_data[:, tempo].shape[-1])


MaxFreq = 4*60
IndexMaxFreq = 0
while freq[IndexMaxFreq] < MaxFreq:
    IndexMaxFreq = IndexMaxFreq + 1

freq = freq[1:IndexMaxFreq]

###############################################################
# select the time scale of the graphs - uncomment the time scales
###############################################################
figsizex = 5
figsizey = 4

start_freq = 0
end_freq = MaxFreq

##################################################
# the figure where the plots will be
##################################################
figfft, axsfft = plt.subplots(2, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
figfft.subplots_adjust(hspace=0.075, left=0.175, bottom=0.125, right=0.95, top=0.98)


fft_dist = np.fft.fft(raw_data[:, amp])
fft_dist = 2 * fft_dist[1:IndexMaxFreq]/Nsamp

fft_lpf = np.fft.fft(raw_data[:, vd_lpf])
fft_lpf = 2 * fft_lpf[1:IndexMaxFreq]/Nsamp

fft_notch = np.fft.fft(raw_data[:, vd_notch])
fft_notch = 2 * fft_notch[1:IndexMaxFreq]/Nsamp

axsfft[0].plot(freq, np.divide(np.absolute(fft_lpf),np.absolute(fft_dist)),
               color='blue', linewidth=linewidth, linestyle='-', label=r'LPF')
axsfft[0].plot(freq, np.divide(np.absolute(fft_notch),np.absolute(fft_dist)),
               color='red', linewidth=linewidth, linestyle='-', label=r'notch')

axsfft[1].plot(freq, 180/np.pi * np.subtract(np.angle(fft_lpf),np.angle(fft_dist)),
               color='blue', linewidth=linewidth, linestyle='-', label=r'LPF')
axsfft[1].plot(freq, 180/np.pi * np.subtract(np.angle(fft_notch),np.angle(fft_dist)),
               color='red', linewidth=linewidth, linestyle='-', label=r'notch')

#figfft.suptitle('From ideal $v_{d+}$ to notch and LPF $v_{d+}$')

axsfft[0].legend(loc='upper right')
axsfft[0].set_ylabel(r'Gain (pu/pu)')
axsfft[1].set_ylabel(r'Phase ($^\circ$)')
axsfft[1].set_xlabel(r'Frequency (Hz)')
axsfft[1].set_xticks(np.arange(0, 300, 30))
axsfft[1].set_xlim(start_freq, end_freq)




##################################################
##################################################
##################################################
# Currents no tempo
##################################################
# the figure where the plots will be
##################################################
figcur, axscur = plt.subplots(3, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
figcur.subplots_adjust(hspace=0.075, left=0.175, bottom=0.125, right=0.95, top=0.98)
linewidth = 0.75

start_time = 0
end_time = 0.1

start_time_index = 0
end_time_index = 0

while raw_data[end_time_index, tempo] < end_time:
    end_time_index = end_time_index + 1

##################################################
# plot 1 - Currents abc
##################################################
axscur[0].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, ia],
            color='red', linewidth=linewidth, linestyle='-',label=r'$a$')
axscur[0].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, ib],
            color='green', linewidth=linewidth, linestyle='-',label=r'$b$')
axscur[0].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, ic],
            color='blue', linewidth=linewidth, linestyle='-',label=r'$c$')
axscur[0].set_xlim(start_time, end_time)
axscur[0].legend(loc='upper right')
axscur[0].set_ylabel(r'Curr. (pu)')
#################################################
# plot 2 - Notch
##################################################
axscur[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, id],
            color='red', linewidth=linewidth, linestyle=':',label=r'$d$')
axscur[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, iq],
            color='blue', linewidth=linewidth, linestyle=':',label=r'$q$')
axscur[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, id_notch],
            color='red', linewidth=linewidth, linestyle='-',label=r'$d+$')
axscur[1].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, iq_notch],
            color='blue', linewidth=linewidth, linestyle='-',label=r'$q+$')
axscur[1].set_xlim(start_time, end_time)
axscur[1].legend(loc='upper right')
axscur[1].set_ylabel(r'Notch (pu)')
#################################################
# plot 3 - LPF
##################################################
axscur[2].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, id],
            color='red', linewidth=linewidth, linestyle=':',label=r'$d$')
axscur[2].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, iq],
            color='blue', linewidth=linewidth, linestyle=':',label=r'$q$')
axscur[2].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, id_lpf],
            color='red', linewidth=linewidth, linestyle='-', label=r'$d+$')
axscur[2].plot(raw_data[start_time_index:end_time_index, tempo],
            raw_data[start_time_index:end_time_index, iq_lpf],
            color='blue', linewidth=linewidth, linestyle='-', label=r'$q+$')
axscur[2].set_xlim(start_time, end_time)
axscur[2].legend(loc='upper right')
axscur[2].set_ylabel(r'LPF (pu)')
axscur[2].set_xlabel(r'Time (s)')

###############################################################
# FFT basics
###############################################################
###############################################################
# select the time scale of the graphs - uncomment the time scales
###############################################################
##################################################
# the figure where the plots will be
##################################################
figfftcur, axsfftcur = plt.subplots(2, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
figfftcur.subplots_adjust(hspace=0.075, left=0.175, bottom=0.125, right=0.95, top=0.98)


fft_dist = np.fft.fft(raw_data[:, id])
fft_dist = 2 * fft_dist[1:IndexMaxFreq]/Nsamp

fft_lpf = np.fft.fft(raw_data[:, id_lpf])
fft_lpf = 2 * fft_lpf[1:IndexMaxFreq]/Nsamp

fft_notch = np.fft.fft(raw_data[:, id_notch])
fft_notch = 2 * fft_notch[1:IndexMaxFreq]/Nsamp

axsfftcur[0].plot(freq, np.divide(np.absolute(fft_lpf),np.absolute(fft_dist)),
               color='red', linewidth=linewidth, linestyle='-', label=r'lpf')
axsfftcur[0].plot(freq, np.divide(np.absolute(fft_notch),np.absolute(fft_dist)),
               color='blue', linewidth=linewidth, linestyle='-', label=r'notch')
#axsfft[0].plot(freq, np.absolute(fft_sig)/np.absolute(fft_dist),color='black', linewidth=linewidth, linestyle='-')

axsfftcur[1].plot(freq, 180/np.pi * np.subtract(np.angle(fft_lpf),np.angle(fft_dist)),
               color='red', linewidth=linewidth, linestyle='-', label=r'lpf')
axsfftcur[1].plot(freq, 180/np.pi * np.subtract(np.angle(fft_notch),np.angle(fft_dist)),
               color='blue', linewidth=linewidth, linestyle='-', label=r'notch')

axsfftcur[1].legend(loc='upper right')
axsfftcur[0].set_ylabel(r'Gain (pu/pu)')
axsfftcur[1].set_ylabel(r'Phase ($^o$)')
axsfftcur[1].set_xlabel(r'Frequency (Hz)')
axsfftcur[1].set_xlim(start_freq, end_freq)


##################################################
# the figure where the plots will be
##################################################
figfftcur0, axsfftcur0 = plt.subplots(2, 1, sharex=True, figsize=(figsizex, figsizey))
# Remove horizontal space between axes
figfftcur0.subplots_adjust(hspace=0.075, left=0.175, bottom=0.125, right=0.95, top=0.98)


fft_dist = np.fft.fft(raw_data[:, id])
fft_dist = 2 * fft_dist[1:IndexMaxFreq]/Nsamp

fft_lpf = np.fft.fft(raw_data[:, id_lpf])
fft_lpf = 2 * fft_lpf[1:IndexMaxFreq]/Nsamp

fft_notch = np.fft.fft(raw_data[:, id_notch])
fft_notch = 2 * fft_notch[1:IndexMaxFreq]/Nsamp

axsfftcur0[0].plot(freq, np.absolute(fft_dist),
               color='black', linewidth=linewidth, linestyle='-', label=r'dist')
axsfftcur0[0].plot(freq, np.absolute(fft_lpf),
               color='red', linewidth=linewidth, linestyle='-', label=r'lpf')
axsfftcur0[0].plot(freq, np.absolute(fft_notch),
               color='blue', linewidth=linewidth, linestyle='-', label=r'notch')


axsfftcur0[1].plot(freq, 180/np.pi * np.angle(fft_dist),
               color='black', linewidth=linewidth, linestyle='-', label=r'dist')
axsfftcur0[1].plot(freq, 180/np.pi * np.angle(fft_lpf),
               color='red', linewidth=linewidth, linestyle='-', label=r'lpf')
axsfftcur0[1].plot(freq, 180/np.pi * np.angle(fft_notch),
               color='blue', linewidth=linewidth, linestyle='-', label=r'notch')

axsfftcur0[1].legend(loc='upper right')
axsfftcur0[0].set_ylabel(r'Gain (pu/pu)')
axsfftcur0[1].set_ylabel(r'Phase ($^o$)')
axsfftcur0[1].set_xlabel(r'Frequency (Hz)')
axsfftcur0[1].set_xlim(start_freq, end_freq)





plt.show()
