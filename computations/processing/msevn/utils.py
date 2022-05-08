import matplotlib as mpl
import seaborn as sns
import matplotlib.pyplot as plt

from .conf.load import plot_config as config

# ------------------------- #

def configure_mpl(config: dict = config) -> None:

    plt.rc('text', usetex=True)
    mpl.rcParams.update(config.get('texrc'))
    plt.rc('text.latex', preamble=r'\usepackage{fouriernc} \usepackage{euscript}')
    sns.set(font_scale=float(config.get('font_scale')), style='white')
    mpl.rcParams.update(config.get('postrc'))

# ------------------------- #