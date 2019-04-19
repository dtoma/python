import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.style.use('seaborn')


def set_size(width, fraction=1):
    """ Set aesthetic figure dimensions to avoid scaling in latex.

    :param float width: Width in pts
    :param float fraction:Fraction of the width which you wish the figure to occupy

    :return fig_dim: Dimensions of figure in inches
    :rtype: Tuple[float, float]
    """
    fig_width_pt = width * fraction
    inches_per_pt = 1 / 72.27
    golden_ratio = (5**.5 - 1) / 2
    fig_width_in = fig_width_pt * inches_per_pt
    fig_height_in = fig_width_in * golden_ratio
    return (fig_width_in, fig_height_in)


width = 345

nice_fonts = {
        # Use LaTex to write all text
        "text.usetex": True,
        "font.family": "serif",
        # Use 10pt font in plots, to match 10pt font in document
        "axes.labelsize": 10,
        "font.size": 10,
        # Make the legend/label fonts a little smaller
        "legend.fontsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
}

mpl.rcParams.update(nice_fonts)

x = np.linspace(0, 2*np.pi, 100)
fig, ax = plt.subplots(1, 1, figsize=set_size(width))
ax.plot(x, np.sin(x))
ax.set_xlim(0, 2*np.pi)
ax.set_xlabel(r'$\theta$')
ax.set_ylabel(r'$\sin{(\theta)}$')

plt.savefig('example_1.pdf', format='pdf', bbox_inches='tight')

fig = plt.figure(figsize=set_size(width))
ax = Axes3D(fig)
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.hot)
ax.contourf(X, Y, Z, zdir='z', offset=-2, cmap=plt.cm.hot)
ax.set_zlim(-2,2)

plt.savefig('plot3d_ex.pdf', format='pdf', bbox_inches='tight')
# plt.show()
