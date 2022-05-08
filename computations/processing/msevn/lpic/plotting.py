import numpy as np
import os
from matplotlib import ticker
import matplotlib.pyplot as plt
from ..conf.load import plot_config as config
from .io import read_bytes

# ------------------------- #

def density(
    
        datadir: str, 
        kind: str = 'electron', 
        imagesize: int = 1600, 
        tlim: tuple = (0, 20), # in laser periods
        xlim: tuple = (0, 166), # in cells
        maxne: float = 5, # in critical units
        tstep: float = 2.8, # in fs
        xstep: float = 1.0 # in nm
    
    ):

    postdir = os.path.join(datadir, 'Post')
    
    if kind == 'electron':
        postfile = os.path.join(postdir, 'spacetime-de')
        cbar_label = r'$n_e\,/\,n_c$'
    
    elif kind == 'ion':
        postfile = os.path.join(postdir, 'spacetime-di')
        cbar_label = r'$n_i\,/\,n_c$'
    
    else:
        raise ValueError

    @ticker.FuncFormatter
    def major_formatter(x, pos):
        return r'' + f'${x * maxne / 255:.2f}$'

    density_el = read_bytes(postfile, imagesize)

    xlim = [xstep*k for k in xlim]
    tlim = [tstep*k for k in tlim]

    fig, ax = plt.subplots(figsize=(10, 10))
    aspect = (xlim[1] - xlim[0]) / (tlim[1] - tlim[0])
    dens = ax.imshow(density_el, cmap=config['globalcmap'], origin='lower', extent=[*xlim, *tlim], aspect=aspect)

    cbar = plt.colorbar(dens, fraction=0.0457, pad=0.04)
    cbar.set_label(cbar_label, labelpad=config['axislabel']['labelpad'])
    cbar.locator = ticker.LinearLocator(config['colorbarprops']['ticker.linear'])
    cbar.formatter = major_formatter
    cbar.update_ticks()

    ax.xaxis.set_major_locator(ticker.LinearLocator(6))
    ax.yaxis.set_major_locator(ticker.LinearLocator(6))

    ax.set_xlabel(r'$z,\:\,\rm{nm}$', labelpad=config['axislabel']['labelpad'])
    ax.set_ylabel(r'$t,\:\,\rm{fs}$', labelpad=config['axislabel']['labelpad'])

    return fig

# ------------------------- #

def field(
    
        datadir: str, 
        kind: str = 'abs', 
        imagesize: int = 1600, 
        tlim: tuple = (0, 20), # in laser periods
        xlim: tuple = (0, 166), # in cells
        maxne: float = 5, # in critical units
        tstep: float = 2.8, # in fs
        xstep: float = 1.0 # in nm
    
    ):

    postdir = os.path.join(datadir, 'Post')
    
    if kind == 'abs':
        post_ex = os.path.join(postdir, 'spacetime-ex')
        post_ey = os.path.join(postdir, 'spacetime-ey')
        post_ez = os.path.join(postdir, 'spacetime-ez')
        cbar_label = r'$|\bf{E}_{\it{s}}|$'
    
    
    else:
        raise ValueError

    @ticker.FuncFormatter
    def major_formatter(x, pos):
        return r'' + f'${x * maxne / 255:.2f}$'

    field_ex = read_bytes(post_ex, imagesize)
    field_ey = read_bytes(post_ey, imagesize)
    field_ez = read_bytes(post_ez, imagesize)

    #field_abs = np.sqrt(field_ex ** 2 + field_ey ** 2 + field_ez ** 2)

    xlim = [xstep*k for k in xlim]
    tlim = [tstep*k for k in tlim]

    fig, ax = plt.subplots(figsize=(10, 10))
    aspect = (xlim[1] - xlim[0]) / (tlim[1] - tlim[0])
    dens = ax.imshow(field_ey, cmap=config['globalcmap'], origin='lower', extent=[*xlim, *tlim], aspect=aspect)

    cbar = plt.colorbar(dens, fraction=0.0457, pad=0.04)
    cbar.set_label(cbar_label, labelpad=config['axislabel']['labelpad'])
    cbar.locator = ticker.LinearLocator(config['colorbarprops']['ticker.linear'])
    cbar.formatter = major_formatter
    cbar.update_ticks()

    ax.xaxis.set_major_locator(ticker.LinearLocator(6))
    ax.yaxis.set_major_locator(ticker.LinearLocator(6))

    ax.set_xlabel(r'$z,\:\,\rm{nm}$', labelpad=config['axislabel']['labelpad'])
    ax.set_ylabel(r'$t,\:\,\rm{fs}$', labelpad=config['axislabel']['labelpad'])

    return fig

# ------------------------- #