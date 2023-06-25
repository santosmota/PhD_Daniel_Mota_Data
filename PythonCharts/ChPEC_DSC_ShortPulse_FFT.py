#################################################################
# Generates the the short pulse and the FFT of the
#   notch, DSC, and AMA
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
    csv_full_path = '../Modelos/ChPEC/DSC/ShortPulse_Raw.txt'

    figure_full_path = '../Modelos/ChPEC/PEC_DSC_ShortPulse' + figure_type
    figure_fft_full_path = '../Modelos/ChPEC/PEC_DSC_ShortPulse_FFT' + figure_type

    colunas = ['time', 'vdideal', 'vqideal', 'vdnotch', 'vqnotch', 'vddsc', 'vqdsc', 'vdama', 'vqama', 'va', 'vb', 'vc']

    df = pd.read_csv(csv_full_path, names=colunas, header=None)

    time_scaling = 1000.0

    df['periods'] = df['time'] / Tn

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

    cor_a = pe.cor_dalt['red']
    cor_b = pe.cor_dalt['green']
    cor_c = pe.cor_dalt['blue']

    cor_ideal = 'black'  # pe.cor_dalt['red']
    cor_notch = pe.cor_dalt['red']
    cor_dsc = pe.cor_dalt['blue']
    cor_ama = pe.cor_dalt['green']

    ###############################################################
    # VOLTAGE abc
    ###############################################################
    axes[0].plot(# df['time'] * time_scaling,
                 df['periods'],
                 df['va'],
                 color=cor_a,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_a$')

    axes[0].plot(# df['time'] * time_scaling,
                 df['periods'],
                 df['vb'],
                 color=cor_b,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_b$')

    axes[0].plot(# df['time'] * time_scaling,
                 df['periods'],
                 df['vc'],
                 color=cor_c,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'$v_c$')

    ###############################################################
    # VOLTAGE dq
    ###############################################################
    axes[1].plot(# df['time'] * time_scaling,
                 df['periods'],
                 df['vdideal'],
                 color=cor_ideal,
                 linewidth=line_width,
                 linestyle='dashed',
                 label=r'Ideal')

    axes[1].plot(# df['time'] * time_scaling,
                 df['periods'],
                 df['vdnotch'],
                 color=cor_notch,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'Notch')

    axes[1].plot(# df['time'] * time_scaling,
                 df['periods'],
                 df['vddsc'],
                 color=cor_dsc,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'DSC')

    axes[1].plot(# df['time'] * time_scaling,
                 df['periods'],
                 df['vdama'],
                 color=cor_ama,
                 linewidth=line_width,
                 linestyle=line_style,
                 label=r'AMA')

    ##########################################################################
    # axis limits
    ##########################################################################
    # axes[0].set_xticks(np.arange(0, 20, 2))
    # axes[0].set_xlim([0, 16])
    axes[0].set_xticks(np.arange(0, 1.25, 0.25))
    axes[0].set_xlim([0, 1])
    axes[0].set_xticklabels(['$0T$', '$T/4$', '$T/2$', '$3T/4$', '$T$'])


    axes[0].set_yticks(np.arange(-2.0, 2.0, 0.5))
    axes[0].set_ylim([-1.0, 1.0])

    ##########################################################################
    # axis names
    ##########################################################################
    # axes[1].set_xlabel(r'Time (\si{\milli\second})')
    axes[1].set_xlabel(r'Time (periods $T$ of the grid)')

    axes[0].set_ylabel(r'Voltage $abc$ frame (\si{pu})')
    axes[1].set_ylabel(r'Voltage $d$ axis (\si{pu})')

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

    if figure_type == '.pdf':
        fig.savefig(figure_full_path, format="pdf", bbox_inches="tight")
    elif figure_type == '.eps':
        fig.savefig(figure_full_path, format='eps')

    # plt.show()

    ##########################################################################
    # fft
    ##########################################################################
    time = df['time'].to_numpy()
    Ns = len(time)
    Ts = time[1] - time[0]
    Fs = 1/Ts
    Ttot = Ns * Ts
    Fstep = 1/Ttot



    # freq = Fs * np.fft.fftfreq(time.shape[-1])

    # fft_pulse = np.fft.fft(df['vdideal'].to_numpy())
    # fft_notch = np.fft.fft(df['vdnotch'].to_numpy())
    # fft_dsc = np.fft.fft(df['vddsc'].to_numpy())
    # fft_ama = np.fft.fft(df['vdama'].to_numpy())

    fft_pulse = np.fft.rfft(df['vdideal'].to_numpy())
    fft_notch = np.fft.rfft(df['vdnotch'].to_numpy())
    fft_dsc = np.fft.rfft(df['vddsc'].to_numpy())
    fft_ama = np.fft.rfft(df['vdama'].to_numpy())

    freq = Fstep * range(0, len(fft_pulse))

    harm = freq / Fn

    phase_notch = 180.0 / np.pi * np.subtract(np.angle(fft_notch), np.angle(fft_pulse))
    phase_dsc = 180.0 / np.pi * np.subtract(np.angle(fft_dsc), np.angle(fft_pulse))
    phase_ama = 180.0 / np.pi * np.subtract(np.angle(fft_ama), np.angle(fft_pulse))

    max_angle = 91.0

    for cnt in range(len(freq)):
        if phase_dsc[cnt] > max_angle:
            phase_dsc[cnt] = phase_dsc[cnt] - 360.0

        if phase_ama[cnt] > max_angle:
            phase_ama[cnt] = phase_ama[cnt] - 360.0

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
    axes_fft[0].plot(harm, np.divide(np.absolute(fft_notch), np.absolute(fft_pulse)),
                     color=cor_notch, linewidth=line_width, linestyle=line_style, label=r'Notch')

    axes_fft[0].plot(harm, np.divide(np.absolute(fft_dsc), np.absolute(fft_pulse)),
                     color=cor_dsc, linewidth=line_width, linestyle=line_style, label=r'DSC')

    axes_fft[0].plot(harm, np.divide(np.absolute(fft_ama), np.absolute(fft_pulse)),
                     color=cor_ama, linewidth=line_width, linestyle=line_style, label=r'AMA')

    ##############################################################
    # FFT phase
    ###############################################################
    axes_fft[1].plot(harm, phase_notch,
                     color=cor_notch, linewidth=line_width, linestyle=line_style, label=r'Notch')

    axes_fft[1].plot(harm, phase_dsc,
                     color=cor_dsc, linewidth=line_width, linestyle=line_style, label=r'DSC')

    axes_fft[1].plot(harm, phase_ama,
                     color=cor_ama, linewidth=line_width, linestyle=line_style, label=r'AMA')

    ##########################################################################
    # axis limits
    ##########################################################################
    axes_fft[0].set_xticks(np.arange(0, 20, 1))
    axes_fft[0].set_xlim([0, 12])

    axes_fft[0].set_yticks(np.arange(0, 2.0, 0.5))
    axes_fft[0].set_ylim([0, 1.05])

    axes_fft[1].set_yticks(np.arange(-180, 180, 90))
    axes_fft[1].set_ylim([-180, 95])
    axes_fft[1].set_yticklabels([r'$-\pi$', r'$-\pi/2$', r'$0$', r'$\pi/2$'])

    ##########################################################################
    # axis names
    ##########################################################################
    axes_fft[1].set_xlabel(r'Harmonic (dimensionless)')

    axes_fft[0].set_ylabel(r'Gain (\si{pu}/\si{pu})')
    axes_fft[1].set_ylabel(r'Phase (rad)') #$^\circ$)')

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
    axes_fft[0].legend(loc='center right', frameon=True, prop={'size': 10})
    # axes[1].legend(loc='upper right', frameon=True, prop={'size': 10})

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

