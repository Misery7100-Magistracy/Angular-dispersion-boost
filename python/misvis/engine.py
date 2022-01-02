import pandas as pd
import numpy as np
from typing import Callable, Any

# ------------------------- #

class Engine:

    CBARPROPS = {

        'position' : 'right', 
        'size' : '5%', 
        'pad' : 0.4

    }

    GLOBCMAP = 'hot'
    AXISLABEL = {

        'labelpad' : 15

    }

    TARGET_PLOT = {

        'plot'      : True,
        'radius'    : 8.9,
        'color'     : 'white',
        'alpha'     : 0.1

    }

    # ------------------------- #

    def __init__(
            
            self, 
            loadmethod: Callable,
            fname: str, 
            **kwargs: Any
        
        ) -> None:

        self.data = loadmethod(fname, **kwargs)
    
    # ------------------------- #

    # some methods ???