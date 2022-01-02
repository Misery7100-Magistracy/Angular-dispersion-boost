import pandas as pd
import numpy as np
from typing import Callable, Any

# ------------------------- #

class Engine:

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