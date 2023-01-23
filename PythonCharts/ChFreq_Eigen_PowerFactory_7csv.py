#################################################################
# Generates figures
#   Which contains the eigen values of the power Factory model
#################################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plot_extra as pe

import matplotlib.pyplot as plt
plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams['mathtext.fontset'] = 'cm'  # 'cm' Computer modern # 'dejavuserif', 'dejavusans'
plt.rcParams['font.family'] = 'serif'
# plt.rcParams['font.serif'] = 'cmr10'  # 'https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/font_file.html
plt.rc('axes', unicode_minus=False)
#https://stackoverflow.com/questions/29188757/matplotlib-specify-format-of-floats-for-tick-labels

#https://matplotlib.org/stable/tutorials/text/usetex.html
# Matplotlib's LaTeX support requires a working LaTeX installation
# Text handling through LaTeX is slower than Matplotlib's very capable mathtext,
#  but is more flexible, since different LaTeX packages (font packages, math packages, etc.) can be used.
plt.rcParams['text.usetex'] = 'True'

#############
# solves a warning with a previous syntax
#https://stackoverflow.com/questions/65645194/warning-set-it-to-a-single-string-instead
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath} \usepackage{crimson} \usepackage{siunitx}'
# from matplotlib.ticker import FormatStrFormatter
# from matplotlib.offsetbox import AnchoredText

#####################################################
# plot eigen value charts from a set of csv files
#####################################################
def plot_eigen_from_csvs_3charts(simcount_total=7,
                                 csvfolder="../Modelos/PrimReserveSharingPowFact/20220824"
                               ):
    print("#####################")
    print("Function name: ", plot_eigen_from_csvs_3charts.__name__)

    figeigename = csvfolder + '/ChFreq_Eigen_1_2MW_PowFact.pdf'

    ##########################################################################
    # figure
    ##########################################################################
    figsizex = 5
    figsizey = 6
    fig_eigen, axs_eigen = plt.subplots(3, 1, sharex=False,
                                        figsize=(figsizex, figsizey),
                                        num='Eigen')

    fig_eigen.show()

    # gs = axs_eigen[0, 0].get_gridspec()

    # for ax in axs_eigen[0:, 0]:
    #     ax.remove()

    # axs_eigen_big = fig_eigen.add_subplot(gs[0:, 0])

    ##########################################################################
    # style of the plots
    ##########################################################################
    cores = []
    legendas = []
    marker = []
    estilos = []
    for simcount in range(0, simcount_total, 1):
        if simcount == 0:
            cores.append(pe.cor_dalt['red'])
            legendas.append('GTs')
            marker.append('x')
            estilos.append('-')  # , ':', '-.']
        elif simcount == 1:
            cores.append(pe.cor_dalt['gray'])
            legendas.append('GTs+BTC+FLX')
            marker.append('+')
            estilos.append(':')
        elif simcount == simcount_total - 1:
            cores.append(pe.cor_dalt['blue'])
            legendas.append('BTC+FLX')
            marker.append('*')
            estilos.append('-.')
        else:
            cores.append(pe.cor_dalt['gray'])
            legendas.append('')
            marker.append('+')
            estilos.append(':')

    grossuras = 0.75
    markersize = 5

    # chart_gov_modes = [[17], [17], [17], [17], [20], [20], [26], [26]]


    ##########################################################################
    # plotting the eigen values
    ##########################################################################
    for simcount in range(0, simcount_total, 1):

        csvname = csvfolder + "/eigenvalues_0" + str(simcount) + '.csv'

        df_eigen = pd.read_csv(csvname)

        ##########################################################################
        # plots ei gen values, aux lines, and names
        ##########################################################################
        axs_eigen[0].plot(df_eigen['real'], df_eigen['imag'],
                           color=cores[simcount],
                           label=legendas[simcount],
                           linestyle='None',
                           linewidth=grossuras,
                           marker=marker[simcount],
                           markersize=markersize)

        axs_eigen[1].plot(df_eigen['real'], df_eigen['imag'],
                             color=cores[simcount],
                             label=legendas[simcount],
                             linestyle='None',
                             linewidth=grossuras,
                             marker=marker[simcount],
                             markersize=markersize)

        axs_eigen[2].plot(df_eigen['real'], df_eigen['imag'],
                          color=cores[simcount],
                          label=legendas[simcount],
                          linestyle='None',
                          linewidth=grossuras,
                          marker=marker[simcount],
                          markersize=markersize)

        maxrealred = 100
        maximagred = 150

        mindampforaddnumbers = 0.1
        legendx = 0.55
        legendy = 0.85

        ##########################################################################
        # name replacements, erasing
        ##########################################################################
        df_eigen['names'] = df_eigen['names'].str.replace('GT1govdb,GT2govdb,GT1,GT2', 'Govs,GTs')
        df_eigen['names'] = df_eigen['names'].str.replace('GT1exc,GT2exc,GT1,GT2', 'Excs,GTs')

        df_eigen['names'] = df_eigen['names'].str.replace('BCpll', 'BTCpll')
        df_eigen['names'] = df_eigen['names'].str.replace('FLEXpll', 'FLXpll')
        df_eigen['names'] = df_eigen['names'].str.replace('PLATpll', 'SECpll')

        df_eigen['names'] = df_eigen['names'].str.replace('GT1exc,GT2exc', 'Excs')
        df_eigen['names'] = df_eigen['names'].str.replace('GT1,GT2', 'GTs')
        df_eigen['names'] = df_eigen['names'].str.replace('WT1udcquacctrl,WT1GC', 'WTs')
        df_eigen['names'] = df_eigen['names'].str.replace('ELictrl,ELLR', 'ELC,ELL')
        df_eigen['names'] = df_eigen['names'].str.replace('FCictrl,FCLR', 'FCC,FCL')
        df_eigen['names'] = df_eigen['names'].str.replace('BCiactref,BATLR', 'BTC,BTL')
        df_eigen['names'] = df_eigen['names'].str.replace('ESSGCudcquacctrl,ESSGC', 'ESSGC')


        if simcount == 0:

            ################################################################
            # overview chart
            ################################################################
            n_segments = 200

            pe.plot_root_locus_damping_lines(eigen_real=df_eigen['real'],
                                              eigen_imag=df_eigen['imag'],
                                              axis=axs_eigen[0],  # nzetalines=31,
                                              nzetalines=13,
                                              max_real=maxrealred, max_imag=maximagred,
                                              add_pos_damping_numbers=True,
                                              max_axis='manual',
                                              min_damp_for_adding_numbers=mindampforaddnumbers,
                                              n_segments=n_segments)

            axs_eigen[0].annotate('',
                                  xy=(-45, 15), xycoords='data',
                                  xytext=(-45, 5), textcoords='data',
                                  arrowprops=dict(arrowstyle='simple', # '"->",
                                  connectionstyle="arc3", color='gray'),
                                  )


            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[0],
                                                  modes=[24], # GTs
                                                  xanot_offset=0.0,
                                                  yanot_offset=0.05,
                                                  hor_orient='center',
                                                  vert_orient='bottom',
                                                  text_color='black'
                                                  )

            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[0],
                                                  modes=[37],  # Exc
                                                  xanot_offset=0.25,
                                                  yanot_offset=0.25,
                                                  hor_orient='left',
                                                  vert_orient='bottom',
                                                  text_color='black'
                                                  )

            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[0],
                                                  modes=[39], # WTs
                                                  xanot_offset=0.0,
                                                  yanot_offset=0.5,
                                                  hor_orient='center',
                                                  vert_orient='bottom',
                                                  text_color='black'
                                                  )

            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[0],
                                                  modes=[67],  # ESSGC
                                                  xanot_offset=0.0,
                                                  yanot_offset=0.25,
                                                  hor_orient='center',
                                                  vert_orient='bottom',
                                                  text_color='black'
                                                  )

            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[0],
                                                  modes=[93], # ELC
                                                  xanot_offset=5,
                                                  yanot_offset=0.0,
                                                  hor_orient='left',
                                                  vert_orient='center',
                                                  text_color='black'
                                                  )

            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[0],
                                                  modes=[95],  # FCC
                                                  xanot_offset=5,
                                                  yanot_offset=0.0,
                                                  hor_orient='left',
                                                  vert_orient='bottom',
                                                  text_color='black'
                                                  )

            # annotation for detail (c)
            axs_eigen[0].text(x=df_eigen.iloc[17, df_eigen.columns.get_loc('real')] + 0.0,
                              y=df_eigen.iloc[17, df_eigen.columns.get_loc('imag')] + 0.1,
                              s='(c)',
                              ha='center',
                              va='bottom',
                              color='black')

            ################################################################
            # PLL chart
            ################################################################
            pe.plot_root_locus_damping_lines(eigen_real=df_eigen['real'],
                                              eigen_imag=df_eigen['imag'],
                                              axis=axs_eigen[1],
                                              nzetalines=19,
                                              max_real=5.25, max_imag=3.75,
                                              add_pos_damping_numbers=True,
                                              max_axis='manual',
                                              min_damp_for_adding_numbers=0.76,
                                              max_damp_for_adding_numbers=0.88,
                                              n_segments=1)

            # auxmodes = [[33], [31]]
            # auxyoffsets = [0.05, 0.2]  #
            auxmodes = [[35], [33], [31]]
            auxyoffsets = [0.05, 0.2, 0.35]

            for [auxmod, auxoffset] in zip(auxmodes, auxyoffsets):
                pe.add_root_locus_participation_name(df=df_eigen,
                                                      axis=axs_eigen[1],
                                                      modes=auxmod,
                                                      xanot_offset=0.0,
                                                      yanot_offset=auxoffset,
                                                      hor_orient='center',
                                                      vert_orient='bottom',
                                                      text_color=cores[simcount]
                                                      )

            axs_eigen[1].annotate('',
                                  xy=(-4.25, 3.025), xycoords='data',
                                  xytext=(-4.5, 2.75), textcoords='data',
                                  arrowprops=dict(arrowstyle='simple',  # '"->",
                                                  connectionstyle="arc3", color='gray'),
                                  )

            axs_eigen[1].annotate('',
                                  xy=(-4.65, 2.37), xycoords='data',
                                  xytext=(-4.8, 2.34), textcoords='data',
                                  arrowprops=dict(arrowstyle='simple',  # '"->",
                                                  connectionstyle="arc3", color='gray'),
                                  )

            ################################################################
            # Governor chart
            ################################################################
            pe.plot_root_locus_damping_lines(eigen_real=df_eigen['real'],
                                              eigen_imag=df_eigen['imag'],
                                              axis=axs_eigen[2],
                                              nzetalines=7,
                                              max_real=2.5, max_imag=2,
                                              add_pos_damping_numbers=True,
                                              max_axis='manual',
                                              min_damp_for_adding_numbers=0.3,
                                              max_damp_for_adding_numbers=0.9,
                                              n_segments=1)

            axs_eigen[2].annotate('',
                                  xy=(-1.75, 1.0), xycoords='data',
                                  xytext=(-1.5, 1.45), textcoords='data',
                                  arrowprops=dict(arrowstyle='simple',  # '"->",
                                                  connectionstyle="arc3", color='gray'),
                                  )

            axs_eigen[2].annotate('',
                                  xy=(-1.75, -1.1), xycoords='data',
                                  xytext=(-1.5, -1.55), textcoords='data',
                                  arrowprops=dict(arrowstyle='simple',  # '"->",
                                                  connectionstyle="arc3", color='gray'),
                                  )


            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[2],
                                                  modes=[0, 5],
                                                  xanot_offset=0.0,
                                                  yanot_offset=0.04,
                                                  hor_orient='center',
                                                  vert_orient='bottom',
                                                  text_color='black'
                                                  )

            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[2],
                                                  modes=[17],
                                                  xanot_offset=-0.03,
                                                  yanot_offset=0.04,
                                                  hor_orient='right',
                                                  vert_orient='bottom',
                                                  text_color=cores[simcount]
                                                  )


            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[2],
                                                  modes=[18],
                                                  xanot_offset=0.025,
                                                  yanot_offset=-0.05,
                                                  hor_orient='right',
                                                  vert_orient='top',
                                                  text_color=cores[simcount]
                                                  )

            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[2],
                                                  modes=[1, 6],
                                                  xanot_offset=0.025,
                                                  yanot_offset=-0.05,
                                                  hor_orient='center',
                                                  vert_orient='top',
                                                  text_color='black'
                                                  )

        if simcount == 5:
            ################################################################
            # Governor chart
            ################################################################
            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[2],
                                                  modes=[20],
                                                  xanot_offset=0.025,
                                                  yanot_offset=0.04,
                                                  hor_orient='right',
                                                  vert_orient='bottom',
                                                  text_color=cores[simcount]
                                                  )

            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[2],
                                                  modes=[21],
                                                  xanot_offset=0.025,
                                                  yanot_offset=-0.05,
                                                  hor_orient='right',
                                                  vert_orient='top',
                                                  text_color=cores[simcount]
                                                  )

        if simcount == 6:
            ################################################################
            # Overview Chart
            ################################################################
            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[0],
                                                  modes=[94],  # BTC
                                                  xanot_offset=0,
                                                  yanot_offset=1,
                                                  hor_orient='center',
                                                  vert_orient='bottom',
                                                  text_color=cores[simcount]
                                                  )

            axs_eigen[0].text(x=df_eigen.iloc[29, df_eigen.columns.get_loc('real')] + 0.025,
                              y=df_eigen.iloc[29, df_eigen.columns.get_loc('imag')] + 0.0,
                              s='(b)',
                              ha='left',
                              va='bottom',
                              color='black')


            ################################################################
            # PLL chart
            ################################################################
            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[1],
                                                  modes=[29], # BTCpll FLXpll, less damped
                                                  xanot_offset=-0.025,
                                                  yanot_offset=0.0,
                                                  hor_orient='right',
                                                  vert_orient='top',
                                                  text_color=cores[simcount]
                                                  )

            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[1],
                                                  modes=[31],
                                                  xanot_offset=0.025,
                                                  yanot_offset=0.0,
                                                  hor_orient='left',
                                                  vert_orient='bottom',
                                                  text_color=cores[simcount]
                                                  )

            pe.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[1],
                                                  modes=[35],
                                                  xanot_offset=0.0,
                                                  yanot_offset=-0.05,
                                                  hor_orient='center',
                                                  vert_orient='top',
                                                  text_color=cores[simcount]
                                                  )

    ##########################################################################
    # axis big
    ##########################################################################
    # axs_eigen[0].grid(which='major', axis='both', linestyle=':', linewidth=0.5, color='gray')

    axs_eigen[0].set_xscale('symlog',
                             linthresh=10,
                             subs=np.arange(2, 10),
                             linscale=0.75)
    axs_eigen[0].set_xlim([-maxrealred, 0])
    axs_eigen[0].set_xticks([-maxrealred, -100, -10, -8, -6, -4, -2, 0])
    axs_eigen[0].set_xticklabels([-maxrealred, -100, -10, -8, -6, -4, -2, 0])

    axs_eigen[0].set_yscale('symlog',
                             linthresh=10,
                             subs=np.arange(2, 10),
                             linscale=1)
    axs_eigen[0].set_yticks([-2, 0, 2, 4, 8, 6, 8, 10, 100, maximagred])
    axs_eigen[0].set_yticklabels([-2, 0, 2, 4, 8, 6, 8, 10, 100, maximagred])
    axs_eigen[0].set_ylim([-2.0, maximagred])

    # axs_eigen[0].legend(loc=(legendx, legendy), frameon=True)  # ax.legend(loc=l, bbox_to_anchor=(0.6,0.5))

    # axs_eigen[0].set_xlabel(r'Real (Np/s)')
    axs_eigen[0].set_ylabel(r'\textbf{(a) Overview}' '\n' r'Imaginary (rad/s)')


    ##########################################################################
    # axis middle
    ##########################################################################
    axs_eigen[1].set_xticks(np.arange(-6, -3, 0.25))
    axs_eigen[1].set_xlim([-5.25, -3.75])

    axs_eigen[1].set_yticks(np.arange(1, 4, 0.25))
    axs_eigen[1].set_ylim([2, 3.75])

    # axs_eigen[1].set_xlabel(r'Real (Np/s)')
    axs_eigen[1].set_ylabel(r'\textbf{(b) Detail PLLs}' '\n' r'Imaginary (rad/s)')

    ##########################################################################
    # axis right
    ##########################################################################
    axs_eigen[2].set_xlim([-2.5, 0])
    axs_eigen[2].set_ylim([-2, 2])

    axs_eigen[2].set_xlabel(r'Real (Np/s)')
    axs_eigen[2].set_ylabel( r'\textbf{(c) Detail Governors}' '\n' r'Imaginary (rad/s)')

    fig_eigen.tight_layout()

    fig_eigen.savefig(figeigename, format='pdf')

    plt.show()



#####################################################
# main
#####################################################
def main():
    print("#####################")
    print("Function name: ", main.__name__)

    plot_eigen_from_csvs_3charts()

if __name__ == '__main__':
    main()

