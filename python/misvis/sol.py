import pandas as pd
import numpy as np
from .engine import Engine

# ------------------------- #

class SolEngine:

    # ------------------------- #

    def __init__(
            
            self,
            fname: str, 
            **kwargs
        
        ) -> None:

        super().__init__(
            
                loadmethod=pd.read_csv, 
                fname=fname, 
                **kwargs
            
            )

    # ------------------------- #

    # def get_value(self, name: str) -> object:
    #     return float(self.data.get(name)[0, 0])

    # # ------------------------- #

    # def get_array(self, name: str) -> object:
    #     return self.data.get(name).astype(np.float64)