from scipy.io import loadmat
from .engine import Engine
from .utils import configure_mpl
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------- #

class MatEngine(Engine):

    def __init__(
            
            self,
            fname: str, 
            **kwargs
        
        ) -> None:

        super().__init__(
            
                loadmethod=loadmat, 
                fname=fname, 
                **kwargs
            
            ) 

    # ------------------------- #

    def get_value(self, name: str) -> object:

        return float(self.data.get(name)[0, 0])

    # ------------------------- #

    def get_array(self, name: str) -> object:

        return self.data.get(name).astype(np.float64)

# ------------------------- #

class MSTM(MatEngine):

    CIRCLE_PTS = 181

    TARGET_PLOT = {

        'plot'      : True,
        'pt_reduce' : 1,
        'alpha'     : 0.1,
        'color'     : 'white'
    }

    # ------------------------- #

    def __init__(self, fname: str, **kwargs) -> None:

        super().__init__(fname, **kwargs)

        self.field = self.get_array('heatmap')
        self.field = self.field[::-1, :]

        self.circles = pd.DataFrame(self.get_array('particles_xy'))
        self.circles.rename(
            
            columns={0 : 'x', 1 : 'y'}, 
            inplace=True
            
        )
        self.circles.drop_duplicates(['x', 'y'])
    
    # ------------------------- #

    def plot_field(
        
            self, 
            trim: int = 0,
            angles: tuple = tuple(),
            target: dict = dict(),
            font_scale: float = 2.0,
            xtick: float = None,
            ytick: float = None, 
            **kwargs
        
        ) -> tuple:

        pltdata = self.field[trim:-trim, trim:-trim] if trim > 0 else self.field
        extval = self.grid_max - self.grid_step * trim
        extent = [-extval, extval] * 2

        configure_mpl(font_scale=font_scale)

        fig, ax = plt.subplots(**kwargs)
        field = ax.imshow(pltdata, cmap='hot', extent=extent)

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.4)
        plt.colorbar(field, cax=cax)

        target = {**self.TARGET_PLOT, **target}

        if target.get('plot'):

            for i in range(0, self.circles.shape[0], self.CIRCLE_PTS):
                x = self.circles.loc[i : i + self.CIRCLE_PTS - 1 : target.get('pt_reduce')].x
                y = self.circles.loc[i : i + self.CIRCLE_PTS - 1 : target.get('pt_reduce')].y

                ax.plot(
                    
                    x, y, 
                    linewidth=0.05, 
                    color=target.get('color'), 
                    alpha=target.get('alpha')
                    
                )
        
        for ang in angles:

            self.add_sc_line(ang, ax, extval)
        
        ax.set_xlabel(r'$x$, $\rm{nm}$', labelpad=15)
        ax.set_ylabel(r'$z$, $\rm{nm}$', labelpad=15)

        if xtick: 
            
            ax.xaxis.set_major_locator(ticker.MultipleLocator(xtick))

        if ytick: 
            
            ax.yaxis.set_major_locator(ticker.MultipleLocator(ytick))
        
        return fig, ax
    
    # ------------------------- #

    def add_sc_line(
            
            self, 
            angle: float, 
            ax: object, 
            extval: float
        
        ) -> None:

        posangle = 360 - angle if angle < 0 else angle
        oppleg = np.tan(angle % 45 * np.pi / 180) * extval

        div = (posangle + 45) // 90
        sign = 1 if div in [1, 2] else -1
        extval *= sign

        oppsign = (2 * int((angle - 90 * div) > 0) - 1) * (2 * int(div < 2) - 1)
        oppleg *= oppsign
        
        y = (1 - div % 2) * extval + (div % 2) * oppleg
        x = (div % 2) * extval + (1 - div % 2) * oppleg

        ax.plot(
            
            [0, x], 
            [0, y], 
            color='white', 
            linestyle='dotted', 
            linewidth=0.5
        
        )

    # ------------------------- #

    @property
    def grid_max(self):

        return self.get_value('grid_max')
    
    # ------------------------- #

    @property
    def grid_step(self):

        return self.get_value('grid_step')
    
    # ------------------------- #