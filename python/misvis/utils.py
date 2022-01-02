import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# ------------------------- #

GITHUB_PALETTE = [
    
    '#4078c0',
    '#6cc644',
    '#bd2c00',
    '#c9510c',
    '#6e5494'
    
]

RCDICT = {
    
    'grid.linewidth'    : 1,
    'xtick.major.size'  : 0,
    'ytick.major.size'  : 0,
    'xtick.minor.size'  : 0,
    'ytick.minor.size'  : 0 
    
}

TEXRC = {

    "mathtext.fontset"  : "custom",
    "font.weight"       : "light",
    "font.serif"        : "New Century Schoolbook",
    "font.family"       : "New Century Schoolbook",
    "font.cursive"      : "New Century Schoolbook",
    "mathtext.rm"       : "New Century Schoolbook",
    "mathtext.it"       : "New Century Schoolbook:italic",
    "mathtext.bf"       : "New Century Schoolbook"

}

# ------------------------- #

def configure_mpl(font_scale: float = 2.0):

    global TEXRC

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r"\usepackage{fouriernc}")

    mpl.rcParams.update(TEXRC)
    sns.set(font_scale=font_scale, style='white')