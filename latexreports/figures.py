import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.style.use('seaborn')
CMAP = plt.get_cmap('cubehelix')


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
    # Set a colormap
    'image.cmap': 'cubehelix',
}

mpl.rcParams.update(nice_fonts)

# 2D bar plot

n = 12
X = np.arange(n)
Y1 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)
Y2 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)

fig = plt.figure(figsize=set_size(width))
plt.axes([0.025,0.025,0.95,0.95])
plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')

for x,y in zip(X,Y1):
    plt.text(x, y+0.05, '%.2f' % y, ha='center', va= 'bottom')

for x,y in zip(X,Y2):
    plt.text(x, -y-0.05, '%.2f' % y, ha='center', va= 'top')

plt.xlim(-.5,n), plt.xticks([])
plt.ylim(-1.25,+1.25), plt.yticks([])

plt.savefig('bar_ex.pdf', format='pdf', bbox_inches='tight', dpi=48)

# 3D figure

fig = plt.figure(figsize=set_size(width))
ax = Axes3D(fig)
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=CMAP)
ax.contourf(X, Y, Z, zdir='z', offset=-2)
ax.set_zlim(-2,2)

plt.savefig('plot3d_ex.pdf', format='pdf', bbox_inches='tight')
