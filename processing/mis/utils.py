import matplotlib as mpl
import seaborn as sns
import matplotlib.pyplot as plt
import yaml
import os

# ------------------------- #

def configure_mpl(config: str = './mis/conf/plotting.yml') -> None:

    with open(os.path.relpath(config), 'r') as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)

    plt.rc('text', usetex=True)
    mpl.rcParams.update(conf.get('texrc'))
    plt.rc('text.latex', preamble=r'\usepackage{fouriernc}')
    sns.set(font_scale=float(conf.get('font_scale')), style='white')

# ------------------------- #