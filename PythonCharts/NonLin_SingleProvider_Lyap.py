import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from matplotlib import cm

plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams['mathtext.fontset'] = 'cm'  # 'cm' Computer modern # 'dejavuserif', 'dejavusans'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'cmr10'
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

plt.rc('axes', unicode_minus=False)



###############################################################
# Annotations in 3D charts
# source: # https://gist.github.com/WetHat/1d6cd0f7309535311a539b42cccca89c
###############################################################
from mpl_toolkits.mplot3d.proj3d import proj_transform
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.text import Annotation

class Annotation3D(Annotation):

    def __init__(self, text, xyz, *args, **kwargs):
        super().__init__(text, xy=(0, 0), *args, **kwargs)
        self._xyz = xyz

    def draw(self, renderer):
        x2, y2, z2 = proj_transform(*self._xyz, self.axes.M)
        self.xy = (x2, y2)
        super().draw(renderer)

def _annotate3D(ax, text, xyz, *args, **kwargs):
    '''Add anotation `text` to an `Axes3d` instance.'''

    annotation = Annotation3D(text, xyz, *args, **kwargs)
    ax.add_artist(annotation)

setattr(Axes3D, 'annotate3D', _annotate3D)

def superficies():
    ################################
    H = 2.5
    k = 4.0 / 88.0 * 50.0
    T = 0.5
    p = 0.0

    ################################
    f_range = np.linspace(-0.1, 0.1, 100)
    pfcr_range = np.linspace(-0.2, 0.2, 100)

    ################################
    f, pfcr = np.meshgrid(f_range, pfcr_range)  # creates the x and y matrices for the surface

    # V = 0.5 * (f * f * 2.0 * H + k * pfcr * pfcr)

    Vdot = f * ((pfcr - p)/(f + 1)) + k * pfcr * (-k * f - pfcr) / T

    # Vdot = (f * pfcr - f * p) / (f + 1.0) + (k * pfcr * (-k*f - pfcr) / T)

    ###############################################################
    # size of the figure (in inches)
    ###############################################################
    figsizex = 5.5
    figsizey = 4.0  # 4.25

    fig, axes = plt.subplots(1, 1, sharex=True,
                             figsize=(figsizex, figsizey),
                             num='Lyapunov',
                             subplot_kw={"projection": "3d"})

    ###############################################################
    # Surface plots
    ###############################################################
    surf_V = axes.plot_surface(f, pfcr, Vdot, cmap=cm.turbo, alpha=0.75,
                                 linewidth=0.0, antialiased=False)

    ###############################################################
    # axis titles and annotations
    ###############################################################
    axes.set_ylabel(r'$p_{FCR}$ (pu/pu)')
    axes.set_xlabel(r'$\widetilde{f}$ (pu)')
    axes.set_zlabel(r'$V$')

    ###############################################################
    # tight layout an show
    ###############################################################
    # axes.view_init(elev=10.0, azim=30.0, roll=0.0)
    # axes.view_init(elev=22.0, azim=13.0, roll=0.0)

    clb = fig.colorbar(surf_V, shrink=0.6, aspect=20)
    clb.ax.set_title('$V$')

    fig.tight_layout()
    # fig.savefig('notready.pdf', format='pdf')

    plt.show()

def curvas_nivel():
    a = 2

    ################################
    H = 2.5
    k = 4.0 / 88.0 * 50.0
    T = 0.05
    p = 0.0

    ################################
    f_range = np.linspace(-0.2, 0.2, 100)
    pfcr_range = np.linspace(-0.2, 0.2, 100)

    ################################
    f, pfcr = np.meshgrid(f_range, pfcr_range)  # creates the x and y matrices for the surface

    # V = 0.5 * (f * f * 2.0 * H + k * pfcr * pfcr)

    Vdot = f * ((pfcr - p) / (f + 1)) - k * pfcr * f - pfcr * pfcr

    ###############################################################
    # size of the figure (in inches)
    ###############################################################
    figsizex = 5.5
    figsizey = 4.0  # 4.25

    fig, axes = plt.subplots(1, 1, sharex=True,
                             figsize=(figsizex, figsizey),
                             num='Lyapunov')

    ###############################################################
    # countour plot
    ###############################################################
    level_V = axes.contour(f, pfcr, Vdot, linewidths=0.75, cmap=cm.turbo)
    axes.clabel(level_V)
    # level_V = axes.contour(f, pfcr, Vdot, levels=[-1, 0, 1])
    # level_V = axes.contourf(f, pfcr, Vdot, vmax=0)  # , vmin=-10, cmap=cm.turbo)

    ###############################################################
    # axis titles and annotations
    ###############################################################
    axes.set_ylabel(r'$p_{FCR}$ (pu/pu)')
    axes.set_xlabel(r'$\widetilde{f}$ (pu)')
    # axes.set_zlabel(r'$V$')

    ###############################################################
    # tight layout an show
    ###############################################################
    # axes.view_init(elev=10.0, azim=30.0, roll=0.0)
    # axes.view_init(elev=22.0, azim=13.0, roll=0.0)

    # clb = fig.colorbar(surf_V, shrink=0.6, aspect=20)
    # clb.ax.set_title('$V$')

    fig.tight_layout()
    # fig.savefig('notready.pdf', format='pdf')

    plt.show()



def main():
    # superficies()

    curvas_nivel()


if __name__ == '__main__':
    main()
