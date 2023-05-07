#################################################################
# Generates the FFTs of two DSC with contiguous delays
#   of the COMPEL - DSC paper
#################################################################

import numpy as np
import pandas as pd
import plot_extra as pe

import matplotlib.pyplot as plt
plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams['mathtext.fontset'] = 'cm'  # 'cm' Computer modern # 'dejavuserif', 'dejavusans'
plt.rcParams['font.family'] = 'serif'
plt.rc('axes', unicode_minus=False)
plt.rcParams['text.usetex'] = 'True'

#############
# solves a warning with a previous syntax
#https://stackoverflow.com/questions/65645194/warning-set-it-to-a-single-string-instead
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath} \usepackage{crimson} \usepackage{siunitx}'
# from matplotlib.ticker import FormatStrFormatter
# from matplotlib.offsetbox import AnchoredText


def plot_chart(figure_type='.pdf'):
    print("#####################")
    print("Function name: ", plot_chart.__name__)

    Fn = 60.0
    Tn = 1.0 / Fn

    ###############################################################
    # CASES - file names - chart limits
    ###############################################################
    csv_full_path = '../Modelos/ChPEC/DSC/FreqAdaptiveFFT_Raw.txt'

    figure_fft_full_path = '../Modelos/ChPEC/PEC_DSC_TwoFFTs' + figure_type

    colunas = ['time', 'i', 'c', 'f', 'w']

    df = pd.read_csv(csv_full_path, names=colunas, header=None)

    ###############################################################
    # size of the figure (in inches), and linestyles
    ###############################################################
    figsizex = 5
    figsizey = 3
    fig, axes = plt.subplots(2, 1, sharex=True,
                             figsize=(figsizex, figsizey),
                             num='Charts')

    line_width = 0.75
    line_style = 'solid'

    cor_i = 'black'
    cor_c = pe.cor_dalt['red']
    cor_f = pe.cor_dalt['blue']
    cor_w = pe.cor_dalt['green']

    ###############################################################
    # INPUT
    ###############################################################
    axes[0].plot(df['time'],
                 df['i'],
                 color=cor_i,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'input')

    ###############################################################
    # OUTPUTS
    ###############################################################
    axes[1].plot(df['time'],
                 df['c'],
                 color=cor_c,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'ceil')

    axes[1].plot(df['time'],
                 df['f'],
                 color=cor_f,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'floor')

    axes[1].plot(df['time'],
                 df['w'],
                 color=cor_w,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'weigthed')

    ##########################################################################
    # axis limits
    ##########################################################################
    # axes[0].set_xticks(np.arange(0, 1.25, 0.25))
    # axes[0].set_xlim([0, 1])
    # axes[0].set_xticklabels(['$0T$', '$T/4$', '$T/2$', '$3T/4$', '$T$'])


    # axes[0].set_yticks(np.arange(-2.0, 2.0, 0.5))
    # axes[0].set_ylim([-1.0, 1.0])

    ##########################################################################
    # axis names
    ##########################################################################
    # axes[1].set_xlabel(r'Time (\si{\milli\second})')
    axes[1].set_xlabel(r'Time (periods $T$ of the grid)')

    axes[0].set_ylabel(r'Input (\si{pu})')
    axes[1].set_ylabel(r'Output (\si{pu})')

    ##########################################################################
    # chart identification - legend - abcdefghi
    ##########################################################################
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    # colors lightgray gray aliceblue whitesmoke
    corlegenda = 'whitesmoke'
    #
    # axes[0].annotate(r'a', xy=(0.7, 0.82), xycoords='axes fraction',
    #                  bbox=dict(boxstyle='circle', fc=corlegenda))

    # axes[1].annotate(r'b', xy=(0.7, 0.82), xycoords='axes fraction',
    #                  bbox=dict(boxstyle='circle', fc=corlegenda))

    ##########################################################################
    # axis legends
    ##########################################################################
    axes[0].legend(loc='upper right', frameon=True, prop={'size': 10})
    axes[1].legend(loc='upper right', frameon=True, prop={'size': 10})

    ##########################################################################
    # align, tighten, shown and save
    ##########################################################################
    fig.align_ylabels(axes[:])
    fig.tight_layout()

    # if figure_type == '.pdf':
    #     fig.savefig(figure_full_path, format="pdf", bbox_inches="tight")
    # elif figure_type == '.eps':
    #     fig.savefig(figure_full_path, format='eps')

    # plt.show()

    ##########################################################################
    # fft
    ##########################################################################
    time = df['time'].to_numpy()
    Ts = time[1] - time[0]
    Fs = 1 / Ts

    samples_in_period = len(time)
    FFT_extra_window = 50.0 - Tn
    FFT_extra_samples = int(np.ceil(FFT_extra_window / Ts))

    trailing_zeros = np.zeros(FFT_extra_samples)

    i = np.concatenate((df['i'].to_numpy(), trailing_zeros), axis=0)
    c = np.concatenate((df['c'].to_numpy(), trailing_zeros), axis=0)
    f = np.concatenate((df['f'].to_numpy(), trailing_zeros), axis=0)
    w = np.concatenate((df['w'].to_numpy(), trailing_zeros), axis=0)

    Ns = len(i)
    Ttot = Ns * Ts
    Fstep = 1/Ttot

    fft_i = np.fft.rfft(i)
    fft_c = np.fft.rfft(c)
    fft_f = np.fft.rfft(f)
    fft_w = np.fft.rfft(w)

    freq = Fstep * range(0, len(fft_i))

    harm = freq / Fn

    gain_c = np.divide(np.absolute(fft_c), np.absolute(fft_i))
    gain_f = np.divide(np.absolute(fft_f), np.absolute(fft_i))
    # gain_w = np.divide(np.absolute(fft_w), np.absolute(fft_i))

    phase_c = np.subtract(np.angle(fft_c), np.angle(fft_i))
    phase_f = np.subtract(np.angle(fft_f), np.angle(fft_i))
    # phase_w = np.subtract(np.angle(fft_w), np.angle(fft_i))

    max_angle = 2*np.pi + 0.001

    # for cnt in range(len(freq)):
    #     if phase_c[cnt] > max_angle:
    #         phase_c[cnt] = phase_c[cnt] - 2.0*np.pi

    #     if phase_f[cnt] > max_angle:
    #         phase_f[cnt] = phase_f[cnt] - 2.0*np.pi

        # if phase_w[cnt] > max_angle:
        #     phase_w[cnt] = phase_w[cnt] - 2.0*np.pi

    ##############################################################
    # size of the figure (in inches), and linestyles
    ###############################################################
    figsizex = 5
    figsizey = 3
    fig_fft, axes_fft = plt.subplots(2, 1, sharex=True,
                             figsize=(figsizex, figsizey),
                             num='FFT')

    ##############################################################
    # FFT amplitude
    ###############################################################
    axes_fft[0].plot(freq, gain_c,
                     color=cor_c, linewidth=line_width, linestyle=line_style, label=r'ceil')

    axes_fft[0].plot(freq, gain_f,
                     color=cor_f, linewidth=line_width, linestyle=line_style, label=r'floor')

    # axes_fft[0].plot(freq, gain_w,
    #                  color=cor_w, linewidth=line_width, linestyle=line_style, label=r'w')

    ##############################################################
    # FFT phase
    ###############################################################
    axes_fft[1].plot(freq, phase_c,
                     color=cor_c, linewidth=line_width, linestyle=line_style, label=r'$n_c = 75$')

    axes_fft[1].plot(freq, phase_f,
                     color=cor_f, linewidth=line_width, linestyle=line_style, label=r'$n_f = 74$')

    # axes_fft[1].plot(freq, phase_w,
    #                  color=cor_w, linewidth=line_width, linestyle=line_style, label=r'w')

    ##########################################################################
    # axis limits
    ##########################################################################
    axes_fft[0].set_xticks(np.arange(110, 130, 1))
    axes_fft[0].set_xlim([118, 124])

    axes_fft[0].set_yticks(np.arange(0, 0.1, 0.025))
    axes_fft[0].set_ylim([0, 0.05])

    axes_fft[1].set_yticks([-np.pi/2, -np.pi/4, 0, np.pi/4, np.pi/2])
    # axes_fft[1].set_ylim([-np.pi, np.pi])
    axes_fft[1].set_yticklabels(['$-\pi/2$', '$-\pi/4$', '$0$', '$\pi/4$', '$\pi/2$'])

    ##########################################################################
    # axis names
    ##########################################################################
    axes_fft[1].set_xlabel(r'Frequency (Hz)')

    axes_fft[0].set_ylabel(r'Gain (\si{pu}/\si{pu})')
    axes_fft[1].set_ylabel(r'Phase (\si{\radian})')

    ##########################################################################
    # chart identification - legend - abcdefghi
    ##########################################################################
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    # colors lightgray gray aliceblue whitesmoke
    corlegenda = 'whitesmoke'
    #
    # axes_fft[0].annotate(r'a', xy=(0.7, 0.82), xycoords='axes fraction',
    #                 bbox=dict(boxstyle='circle', fc=corlegenda))

    # axes_fft[1].annotate(r'b', xy=(0.7, 0.82), xycoords='axes fraction',
    #                 bbox=dict(boxstyle='circle', fc=corlegenda))

    ##########################################################################
    # axis legends
    ##########################################################################
    # axes_fft[0].legend(loc='center right', frameon=True, prop={'size': 10})
    axes_fft[1].legend(loc='center right', frameon=True, prop={'size': 10})

    ##########################################################################
    # align, tighten, shown and save
    ##########################################################################
    fig_fft.align_ylabels(axes_fft[:])
    fig_fft.tight_layout()

    if figure_type == '.pdf':
        fig_fft.savefig(figure_fft_full_path, format="pdf", bbox_inches="tight")
    elif figure_type == '.eps':
        fig_fft.savefig(figure_fft_full_path, format='eps')

    ##########################################################################
    # show plot
    ##########################################################################
    plt.show()


#####################################################
# main
#####################################################
def main():
    print("#####################")
    print("Function name: ", main.__name__)

    plot_chart()

if __name__ == '__main__':
    main()

