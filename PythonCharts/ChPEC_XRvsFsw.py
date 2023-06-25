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

def plotchart ():

    Fn = 50.0
    Wn = 2 * np.pi * Fn

    Fsws = np.arange(start=2500.0, stop=4050.0, step=50.0)
    n_samp = len(Fsws)

    Lrs = np.zeros(n_samp)
    Fres = np.zeros(n_samp)
    Rc = np.zeros(n_samp)

    Sgen = 88e6
    Vgen = 11e3
    Zbgen = Vgen**2 / Sgen

    Xdgen = 0.299 * Zbgen
    Rsgen = 0.0242 * Zbgen + 0.01  # 10mOhm added for breakers and high voltage swithgear

    Pload = 44e6
    Rload = Vgen**2 / Pload

    Strafo = 10e6
    Vtrafo = 690.0
    Itrafo = Strafo / Vtrafo / 3**0.5
    Zbtrafo = Vtrafo ** 2 / Strafo

    Xtrafo = 0.06 * Zbtrafo
    Ltrafo = Xtrafo / Wn
    Rtrafo = 0.005 * Zbtrafo

    Rreact = 0.01 * Zbtrafo

    Xc = 20 * Zbtrafo
    Cc = 1 / (Wn * Xc)

    Vdc = 1200.0

    for cnt in range(n_samp):
        Lrs[cnt] = Vdc / (0.8 * 2 ** 0.5 * Itrafo * Fsws[cnt])
        Fres[cnt] = (1 / 2 / np.pi) * ((Lrs[cnt] + Ltrafo) / (Lrs[cnt] * Ltrafo * Cc))**0.5
        Rc[cnt] = 1 / (6 * np.pi * Fres[cnt] * Cc)

    xrs = (Wn * Lrs) / Zbtrafo
    rcs = Rc / Zbtrafo

    # print(xrs)
    # print(Fres)
    # print(rcs)

    ##################################################
    # Bases of the converter
    ##################################################
    xd_con = Xdgen / Zbgen * Strafo / Sgen
    rs_con = Rsgen / Zbgen * Strafo / Sgen
    rload_con = Rload / Zbgen * Strafo / Sgen

    xc = Xc / Zbtrafo

    zgen_con = complex(rs_con, xd_con)
    zload_con = complex(rload_con, 0.0)
    zpcc_con = (zgen_con * zload_con) / (zgen_con + zload_con)

    zc_con = np.zeros(n_samp, dtype=complex)
    zr_con = np.zeros(n_samp, dtype=complex)
    ztot_con = np.zeros(n_samp, dtype=complex)
    xoverr = np.zeros(n_samp)

    for cnt in range(n_samp):
        zr_con[cnt] = complex(Rreact / Zbtrafo, xrs[cnt])
        zc_con[cnt] = complex(rcs[cnt], -xc)

        ztot_con[cnt] = (zpcc_con * zc_con[cnt]) / (zpcc_con + zc_con[cnt]) + zr_con[cnt]

        xoverr[cnt] = np.imag(ztot_con[cnt]) / np.real(ztot_con[cnt])

    # print(zpcc_con)
    # print(zr_con)
    # print(zc_con)
    # print(ztot_con)
    # print(xoverr)

    three_tau = 3 * xoverr / Wn

    print(three_tau)

    ###############################################################
    # size of the figure
    ###############################################################
    figsizex = 5
    figsizey = 3

    linewidth = 0.75

    ##################################################
    # the figure where the plots will be
    ##################################################
    fig, axs = plt.subplots(2, 1, sharex=True, figsize=(figsizex, figsizey))

    ##################################################
    # DC link voltage
    ###################################################
    axs[0].plot(Fsws,xoverr,
                color=pe.cor_dalt['blue'], linewidth=linewidth, linestyle='-', label=r'$X/R$')

    axs[1].plot(Fsws,xrs,
                color=pe.cor_dalt['red'], linewidth=linewidth, linestyle='-', label=r'xrs')

    ##########################################################################
    # chart identification - legend - abcdefghi
    ##########################################################################
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    # colors lightgray gray aliceblue whitesmoke
    corlegenda = 'whitesmoke'
    #
    axs[0].annotate(r'a', xy=(0.9, 0.75), xycoords='axes fraction',
                     bbox=dict(boxstyle='circle', fc=corlegenda))

    axs[1].annotate(r'b', xy=(0.9, 0.75), xycoords='axes fraction',
                     bbox=dict(boxstyle='circle', fc=corlegenda))

    ##################################################
    # Legends and titles
    axs[1].set_xticks(np.arange(2500, 5500, 250))
    axs[1].set_xlim(2500, 4000)
    axs[1].set_xlabel(r'ESSGC PWM Switching Frequency (Hz)')

    # axs.legend(loc='upper right', frameon=False)
    axs[0].set_ylabel(r'X/R (pu/pu)')
    axs[0].set_yticks(np.arange(10, 30, 2))
    axs[0].set_ylim(12, 21)

    axs[1].set_ylabel(r'LCL $x_r$ (pu)')
    axs[1].set_yticks(np.arange(0.1, 0.5, 0.05))
    axs[1].set_ylim(0.20, 0.35)


    fig.tight_layout()
    fig.align_ylabels(axs)

    ##################################################
    # saving and showing
    ##################################################
    print('Saving path and file:')
    save_full_file_path = '../Modelos/ChPEC/PEC_XRvsFsw.pdf'
    print(save_full_file_path)
    plt.savefig(save_full_file_path, format='pdf')
    plt.show()

#####################################################
# main
#####################################################
def main():
    print("#####################")
    print("Function name: ", main.__name__)

    plotchart()

if __name__ == '__main__':
    main()
