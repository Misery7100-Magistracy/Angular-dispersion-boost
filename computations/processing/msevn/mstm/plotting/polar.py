from matplotlib import ticker
import matplotlib.pyplot as plt
import numpy as np
from ...conf.load import plot_config as config
from ..equations import *

# ------------------------- #

def e_int(

        e_int_data: np.ndarray,
        dphi: np.ndarray,
        dtheta: np.ndarray,
        kind: str = 't',
        max_hardcoded: float = None,
        no_colorbar: bool = False,
        cbarlabel: str = r'$E_{\rm{int}}$',
        symmertry: bool = True
    ):

    if symmertry:
        p = np.append(dphi, 180 + dphi)
    
    else:
        p = dphi

    if kind == 't':
        t = dtheta
        values = e_int_data
        rticks = list(range(10, 80, 20))
        ticklabs = rticks
        pmesh, tmesh = np.meshgrid(p * np.pi / 180, t)
    
    elif kind == 'r':
        t = dtheta
        values = e_int_data
        rticks = list(range(100, 170, 20))
        ticklabs = rticks[::-1]
        pmesh, tmesh = np.meshgrid(p * np.pi / 180, 270 - t)
    
    if symmertry:
        plot_vals = np.concatenate([values, values[:, ::-1]], axis=1)
    
    else:
        plot_vals = values

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, polar='True')
    ax.grid(True, alpha=0.2, color='black')

    if max_hardcoded is None:
        cax = ax.contourf(
                pmesh, tmesh, 
                plot_vals, 
                cmap='turbo', 
                levels=np.linspace(0, values.max(), 150), 
                zorder=-1
            )
    else:
        cax = ax.contourf(
                pmesh, tmesh, 
                plot_vals, 
                cmap='turbo', 
                levels=np.linspace(0, max_hardcoded, 150), 
                zorder=-1
            )

    ax.set_xlabel(r'$\Delta \varphi$', labelpad=15)
    ax.set_xticklabels([r'$' + str(i) + r'^{\circ}$' for i in range(0, 360, 45)])
    ax.set_rgrids(rticks, angle=45)
    ax.set_yticklabels([r'$' + str(i) + r'^{\circ}$' for i in ticklabs], color='white')
    ax.xaxis.set_tick_params(pad=10)

    if not no_colorbar:
        cbar = plt.colorbar(cax, fraction=0.046, pad=0.1)
        cbar.set_label(cbarlabel, labelpad=15)

        cbar.ax.yaxis.set_major_locator(ticker.LinearLocator(config['colorbarprops']['ticker.linear']))

    rlab = ax.set_ylabel(r'$\Delta \theta$', color='white')
    rlab.set_position((5, 0.6))
    rlab.set_rotation(0)
    ax.yaxis.labelpad = -350

    for c in cax.collections:
        c.set_edgecolor("face")
    
    return fig

# ------------------------- #

def _miller_idx(
        
        function, 
        kind: str = 't', 
        func_kwargs: dict = dict(),
        levels: np.ndarray = np.arange(-10, 10, 1),
        config: dict = dict()
    
    ):

    CONFIG = {
        'grid_color' : 'black',
        'contourf' : True,
        'cmap' : 'turbo',
        'resolution' : 200,
        'labels' : {
            'cbar' : r'$l^\prime$',
            'y' : r'$\theta_0$, $^{\circ}$',
            'x' : r'$\varphi_0$, $^{\circ}$'
        }
    }

    CONFIG.update(config)

    p = np.linspace(0, 360, 180)

    if kind == 't':
        t = np.linspace(0, 90, 180)
        values = np.array([[
            function(tx, px, **func_kwargs) 
            for px in p] 
            for tx in t])
        rticks = list(range(10, 80, 20))
        ticklabs = rticks
    
    elif kind == 'r':
        t = np.linspace(90, 180, 180)
        values = np.array([[
            function(270 - tx, px, **func_kwargs) 
            for px in p] 
            for tx in t])
        rticks = list(range(100, 170, 20))
        ticklabs = rticks[::-1]
    
    else:
        raise ValueError
    
    pmesh, tmesh = np.meshgrid(p * np.pi / 180, t)

    # plotting 

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, polar='True')
    ax.grid(True, alpha=0.2, color=CONFIG['grid_color'])
    
    aa = ax.contour(pmesh, tmesh, values, levels=levels, colors='white', zorder=-1)
    ax.clabel(aa, inline=1)

    if CONFIG['contourf']:

        im = ax.contourf(pmesh, tmesh, values, levels=np.linspace(values.min(), values.max(), CONFIG['resolution']), cmap=CONFIG['cmap'], zorder=-2)

        cbar = plt.colorbar(im, fraction=0.046, pad=0.1)
        cbar.set_label(CONFIG['labels']['cbar'], labelpad=10)
        cbar.ax.yaxis.set_major_locator(ticker.LinearLocator(8))

    ax.set_xlabel(CONFIG['labels']['x'], labelpad=15)
    rlab = ax.set_ylabel(CONFIG['labels']['y'], color='black')
    rlab.set_position((5, 0.6))
    rlab.set_rotation(0)
    ax.yaxis.labelpad = -400

    ax.set_xticklabels([r'$' + str(i) + r'^{\circ}$' for i in range(0, 360, 45)])
    ax.xaxis.set_tick_params(pad=10)
    ax.set_rgrids(rticks, angle=45)
    ax.set_yticklabels([r'$' + str(i) + r'^{\circ}$' for i in ticklabs])

    return fig, ax

# ------------------------- #