import modin.pandas as pd
from .engine import Engine
from .utils import configure_mpl
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt

# ------------------------- #

class SolEngine(Engine):

    # ------------------------- #

    def __init__(
            
            self,
            fname: str, 
            **kwargs
        
        ) -> None:

        super().__init__(

            fname=fname,
            loadmethod=pd.read_csv,  
            **kwargs
        
        )

    # ------------------------- #

    # def get_value(self, name: str) -> object:
    #     return float(self.data.get(name)[0, 0])

    # # ------------------------- #

    # def get_array(self, name: str) -> object:
    #     return self.data.get(name).astype(np.float64)

# ------------------------- #

class ScattInd(SolEngine):

    def __init__(
            
            self, 
            fname: str,
            **kwargs
            
        ) -> None:

        super().__init__(
            
            fname, 
            comment='%', 
            header=None,
            **kwargs
            
        )

# ------------------------- #

class Field2D(SolEngine):

    COLUMNS = {

        0 : 'x',
        1 : 'y',
        2 : 'z'

    }

    # ------------------------- #

    def __init__(
            
            self, 
            fname: str,
            vars: tuple = ('normE',),
            normal: str = 'y',
            **kwargs
            
        ) -> None:

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
    
    # ------------------------- #

    def plot_var(
        
            self, 
            var: str = 'normE',
            trim: int = 0,
            font_scale: float = 2.0,
            xtick: float = None,
            ytick: float = None,
            target: dict = dict(),
            **kwargs
        
        ) -> tuple:

        if var not in self.vars:

            raise ValueError(f'{var} is not in the data')
        
        pltdata = self.data[var][trim:-trim, trim:-trim] if trim > 0 else self.data[var]
        extval = self.grid_max - self.grid_step * trim
        extent = [-extval, extval] * 2

        configure_mpl(font_scale=font_scale)

        fig, ax = plt.subplots(**kwargs)
        field = ax.imshow(pltdata, cmap=self.GLOBCMAP, extent=extent)

        divider = make_axes_locatable(ax)
        cax = divider.append_axes(**self.CBARPROPS)
        plt.colorbar(field, cax=cax)

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

        ax.set_xlabel(r'$' + self.inplane[0] + r'$, $\rm{nm}$', **self.AXISLABEL)
        ax.set_ylabel(r'$' + self.inplane[1] + r'$, $\rm{nm}$', **self.AXISLABEL)

        if xtick: 
            
            ax.xaxis.set_major_locator(ticker.MultipleLocator(xtick))

        if ytick: 
            
            ax.yaxis.set_major_locator(ticker.MultipleLocator(ytick))
        
        return fig, ax
