import pandas as pd
from .engine import Engine as Eng
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import numpy as np
from typing import Callable
from matplotlib import transforms

# ------------------------- #

class Engine(Eng):

    def __init__(self, fname: str, **kwargs):

        super().__init__(
            fname=fname,
            loadmethod=pd.read_csv,  
            **kwargs
        )

# ------------------------- #

class ScattInd(Engine):

    def __init__(self, fname: str, **kwargs):

        super().__init__(
            fname, 
            comment='%', 
            header=None,
            **kwargs
        )

# ------------------------- #

class Field2D(Engine):

    COLUMNS = {

        0 : 'x',
        1 : 'y',
        2 : 'z'

    }

    # ......................... #

    def __init__(
            
            self, 
            fname: str,
            vars: tuple = ('normE',),
            normal: str = 'y',
            **kwargs
            
        ):

        super().__init__(       
            fname,
            comment='%', 
            header=None,
            **kwargs
        )

        rename = {

            **self.COLUMNS, 
            **dict(
                (3 + i, vars[i]) 
                for i in range(len(vars))
                )
            
        }

        self.data.rename(columns=rename, inplace=True)
        self.data.drop(normal, axis=1, inplace=True)

        self.inplane = [x for x in self.COLUMNS.values() if x != normal]
        self.grid_max = self.data[self.inplane].max().max()
        self.grid_step = max(self.data[self.inplane[0]].diff()[1], self.data[self.inplane[1]].diff()[1])

        length = self.data.shape[0]

        transformed_data = dict()

        for v in vars:

            transformed_data[v] = (self.data[v]
                                    .to_numpy()
                                    .reshape(int(length ** 0.5), int(length ** 0.5))
                                    [::-1, :]
                                )
        
        self.data = transformed_data
        self.vars = vars
    
    # ......................... #

    def plot_var(
        
            self, 
            var: str = 'normE',
            trim: int = 0,
            xtick: float = None,
            ytick: float = None,
            target: dict = dict(),
            vmax = 1.,
            vmin = 0.,
            normalize = True,
            bartick: float = 0.1,
            custom_func: Callable = None,
            custom_label: str = r'$|\mathbf{E}_{\it{s}}|^2$',
            custom_x: str = r'$x$, $\rm{nm}$',
            custom_y: str = r'$z$, $\rm{nm}$',
            angle_compensation: float = 0,
            inversion: bool = False,
            factor: float = 1,
            **kwargs
        
        ) -> tuple:

        if var not in self.vars:

            raise ValueError(f'{var} is not in the data')
        
        pltdata = self.data[var][trim:-trim, trim:-trim] if trim > 0 else self.data[var]

        if inversion:
            pltdata = pltdata.T

        if custom_func:
            pltdata = custom_func(pltdata)

        if normalize: 
            pltdata = pltdata / np.amax(pltdata)

        extval = self.grid_max - self.grid_step * trim
        extent = [-extval, extval] * 2


        tr = transforms.Affine2D().rotate_deg(angle_compensation)

        fig, ax = plt.subplots(**kwargs)
        field = ax.imshow(
            pltdata * factor, 
            vmax=vmax,
            vmin=vmin, 
            cmap=self.GLOBCMAP, 
            extent=extent,
            transform=tr + ax.transData
        )

        divider = make_axes_locatable(ax)
        cax = divider.append_axes(**self.CBARPROPS)
        bar = plt.colorbar(field, cax=cax)
        bar.set_label(custom_label, labelpad=15)
        bar.locator = ticker.MultipleLocator(bartick)
        #bar.locator = ticker.LinearLocator(7)
        bar.update_ticks()

        target = {**self.TARGET_PLOT, **target}

        if target.get('plot'):
            circle = plt.Circle(
                    (0, 0), 
                    target.get('radius'), 
                    color=target.get('color'),
                    alpha=target.get('alpha'), 
                    fill=False
                )
            ax.add_patch(circle)

        ax.set_xlabel(custom_x, **self.AXISLABEL)
        ax.set_ylabel(custom_y, **self.AXISLABEL)

        if xtick: 
            ax.xaxis.set_major_locator(ticker.MultipleLocator(xtick))

        if ytick: 
            ax.yaxis.set_major_locator(ticker.MultipleLocator(ytick))

        if inversion:
            ax.invert_xaxis()
        
        return fig, ax

# ------------------------- #
