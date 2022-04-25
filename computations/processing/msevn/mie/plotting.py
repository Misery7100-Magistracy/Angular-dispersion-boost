import yaml
import os
from .equations import *
import matplotlib.pyplot as plt
import seaborn as sns
from ..conf.load import plot_config as config

# ------------------------- #

def scattering_coefficient(

        ne: np.ndarray = np.linspace(0, 5, 20000),
        ka: float = 0.5,
        beta: float = 0,
        orders: list = list(range(1, 4)),
        config: dict = config,
        asymp: bool = True

    ):
    
    palette = config['palette']
    
    orders = orders[:5]
    full = a_n_sph_full
    
    if asymp:
        approx = a_n_sph0

    else:
        approx = a_n_sph1


    fig, ax = plt.subplots(figsize=(10, 6))
    
    for i, o in enumerate(orders):
        
        vals = np.abs( full(ka, o, eps_drude(ne, beta=beta)) )
        sns.lineplot(
            
            x=ne, 
            y=vals, 
            linewidth=1, 
            ax=ax, 
            label=r'$n=%s,\:\: \rm{exact}$' % o, 
            color=palette[i]
        
        )
        
        vals = np.abs( approx(ka, o, eps_drude(ne, beta=beta)) )
        sns.lineplot(
            
            x=ne, 
            y=vals, 
            linewidth=1, 
            ax=ax, 
            label=r'$n=%s,\:\: \rm{asymp}$' % o, 
            color=palette[i],
            linestyle='dotted'
        
        )
    
    ax.set_xlabel(r'$n_e\:/\:n_c$', labelpad=15)
    ax.set_ylabel(r'$|\:a_n\:|$', labelpad=15)

    lgd = ax.legend(loc='lower center', bbox_to_anchor=(0, 1, 1, 0), ncol=3, fontsize=18)
    
    return fig, lgd

# ------------------------- #

def squared_refractive_index(

        ka: np.ndarray = np.linspace(0.01, 5, 20000),
        beta: float = 0,
        orders: list = list(range(1, 4)),
        nenc: bool = False,
        config: dict = config

    ):
    
    """
    """
    
    palette = config['palette']
    
    orders = orders[:5]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    
    for i, o in enumerate(orders):
        
        vals = resonance_m_squared(ka, o)
        
        if nenc:
            vals = np.abs((1 - vals) * complex(1, beta))
            
        sns.lineplot(
            
            x=ka, 
            y=vals, 
            linewidth=1, 
            ax=ax, 
            label=r'$n=%s$' % o, 
            color=palette[i]
        
        )
    
    ax.set_xlabel(r'$ka$', labelpad=15)
    
    if nenc:
        ax.set_ylabel(r'$n_e\:/\:n_c$', labelpad=15)
    else:
        ax.set_ylabel(r'$m^2$', labelpad=15)

    lgd = ax.legend(loc='lower center', bbox_to_anchor=(0, 1, 1, 0), ncol=3, fontsize=18)
    
    return fig, lgd

# ------------------------- #