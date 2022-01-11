import numpy as np
import os
from itertools import product

# ------------------------- #

class MeshGenerator:

    def __init__(self) -> None:

        self.coords = list()
    
    # ------------------------- #

    def build_mesh(
            
            self,
            radius=20., 
            gap=10., 
            edge=10, 
            m=1.497, 
            kind='cube', 
            random=False
        
        ):
        
        if kind == 'cube':

            rng = (2*radius + gap) * (edge - 1) / 2
            coords = np.linspace(-rng, rng, edge)
            coords = np.array(list(map(list, product(coords, repeat=3))))
            output = list(map(lambda x: list(x) + [radius, 0, m], coords))
        
        elif kind == 'plate':

            rng = (2*radius + gap) * (edge - 1) / 2
            coords = np.linspace(-rng, rng, edge)
            coords = np.array(list(map(list, product(coords, repeat=2))))
            output = list(map(lambda x: list(x) + [0, radius, 0, m], coords))
        
        self.coords = output
    
    # ------------------------- #

    def save(self, fname: str = 'particles.txt') -> None:

        path = os.path.join('../matlab', fname)

        with open(path, 'w') as f:
            for l in self.coords:
                f.write(','.join(map(str, l)) + '\n')

        f.close()

# ------------------------- #