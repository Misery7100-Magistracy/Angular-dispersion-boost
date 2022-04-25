import matplotlib as mpl
import seaborn as sns
import matplotlib.pyplot as plt

from .conf.load import plot_config as config

# ------------------------- #

def configure_mpl(config: dict = config) -> None:

    plt.rc('text', usetex=True)
    plt.rcParams['contour.negative_linestyle'] = 'solid'
    mpl.rcParams.update(config.get('texrc'))
    plt.rc('text.latex', preamble=r'\usepackage{fouriernc}')
    sns.set(font_scale=float(config.get('font_scale')), style='white')

# ------------------------- #