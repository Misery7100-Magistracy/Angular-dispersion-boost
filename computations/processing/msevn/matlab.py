from scipy.io import loadmat
from .engine import Engine as Eng
from .utils import configure_mpl
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

# ------------------------- #

class Engine(Eng):

    def __init__(self, fname: str, **kwargs):

        super().__init__(
                loadmethod=loadmat, 
                fname=fname, 
                **kwargs
            ) 

    # ......................... #

    def get_value(self, name: str) -> object:
        return float(self.data.get(name)[0, 0])

    # ......................... #

    def get_array(self, name: str) -> object:
        return self.data.get(name).astype(np.float64)

# ------------------------- #

class MSTM(Engine):

    def __init__(self, fname: str, **kwargs):

        super().__init__(fname, **kwargs)

        self.field = self.get_array('heatmap')
        self.field = self.field[::-1, :]

        self.circles = pd.DataFrame(self.get_array('particles_xy'))
        self.circles.rename(
            columns={0 : 'x', 1 : 'y', 2 : 'z', 3 : 'r'}, 
            inplace=True 
        )
        self.circles.drop_duplicates(['x', 'z', 'r'], inplace=True)
        self.circles.reset_index(drop=True, inplace=True)
    
    # ......................... #

    def plot_field(
        
            self, 
            trim: int = 0,
            angles: List[Tuple[float]] = [],
            target: dict = dict(),
            xtick: float = None,
            ytick: float = None,
            reduce : float = 0.8,
            bartick: float = 0.1,
            external_circles: object = None,
            vmax = 1.,
            vmin = 0.,
            normalize = True, 
            **kwargs
        
        ) -> tuple:

        pltdata = self.field[trim:-trim, trim:-trim] if trim > 0 else self.field

        if normalize: 
            pltdata = pltdata / np.amax(self.field)

        extval = self.grid_max - self.grid_step * trim
        extent = [-extval, extval] * 2

        configure_mpl()

        fig, ax = plt.subplots(**kwargs)
        field = ax.imshow(
                pltdata,
                vmax=vmax,
                vmin=vmin, 
                cmap=self.GLOBCMAP, 
                extent=extent
            )

        bbea = []

        divider = make_axes_locatable(ax)
        cax = divider.append_axes(**self.CBARPROPS)
        bar = plt.colorbar(field, cax=cax)
        bar.locator = ticker.MultipleLocator(bartick)
        bar.update_ticks()

        target = {**self.TARGET_PLOT, **target}

        if target.get('plot'):

            if not external_circles is None:
                for i in range(external_circles.shape[0]):

                    x, _, y, r = external_circles.loc[i]
                    circle = plt.Circle(
                        (x, y), 
                        r, 
                        color=target.get('color'),
                        alpha=target.get('alpha'),
                        linewidth=target.get('linewidth'),
                        fill=False
                    )
                    ax.add_patch(circle)

            else:
                for i in range(self.circles.shape[0]):

                    x, _, y, r = self.circles.loc[i]
                    circle = plt.Circle(
                        (x, y), 
                        r, 
                        color=target.get('color'),
                        alpha=target.get('alpha'),
                        fill=False
                    )
                    ax.add_patch(circle)
        
        for (ang, shift) in angles:
            arrow = self.add_sc_line(ang, ax, extval, reduce=reduce, shift=shift)
            bbea.append(arrow)
        
        xl = ax.set_xlabel(r'$x$, $\rm{nm}$', **self.AXISLABEL)
        yl = ax.set_ylabel(r'$z$, $\rm{nm}$', **self.AXISLABEL)
        
        bbea.append(xl)
        bbea.append(yl)

        if xtick: 
            ax.xaxis.set_major_locator(ticker.MultipleLocator(xtick))

        if ytick: 
            ax.yaxis.set_major_locator(ticker.MultipleLocator(ytick))
        
        return fig, ax, bbea
    
    # ......................... #

    def add_sc_line(
            
            self, 
            angle: float, 
            ax: object, 
            extval: float,
            reduce: float = 0.8,
            shift: float = 0.0
        
        ) -> None:

        angle += 90
        posangle = angle % 360 if angle < 0 else angle

        radius = extval * reduce

        y = radius * np.sin(posangle * np.pi / 180)
        x = radius * np.cos(posangle * np.pi / 180)

        sc = abs(shift * extval)

        if y != 0:
            sqrtdc = np.sqrt(sc ** 2 -  (sc ** 2 - radius ** 2) * (radius / y ) ** 2)
            y1 = y ** 2 * (-sc + sqrtdc) / radius ** 2
            y2 = y ** 2 * (-sc - sqrtdc) / radius ** 2
            yc = max(y1, y2)

        else:
            yc = 0
        

        xc = np.sign(x) * np.sqrt(radius ** 2 - (yc + sc) ** 2)

        return ax.arrow(
            0, shift * extval, 
            xc, yc * np.sign(y), 
            color='white', 
            head_width=radius*0.048, 
            overhang=0.5, 
            linewidth=0.8, 
            linestyle='dotted', 
            length_includes_head=True
        )

    # ......................... #

    @property
    def grid_max(self):

        return self.get_value('grid_max')
    
    # ......................... #

    @property
    def grid_step(self):

        return self.get_value('grid_step')
    
    # ......................... #