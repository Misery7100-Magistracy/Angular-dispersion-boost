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
        
        self.data = output

    # ------------------------- #

    @staticmethod
    def rotate(

            data,
            a=0

        ):

        return data.dot(np.array([

                [np.cos(a), 0, np.sin(a)],
                [0, 1, 0],
                [-np.sin(a), 0, np.cos(a)]
                
            ]))

    # ------------------------- #

    def project_2d(

            self,
            radius=20.,
            gap=10.,
            edge=10.,
            mult=4,
            angle=0

        ):

        angle *= (np.pi / 180)

        rng = (2*radius + gap) * (edge - 1) / 2
        coords1 = np.linspace(-rng, rng, edge)
        coords2 = np.linspace(-rng*mult, rng*mult, edge*mult)
        coords = np.array(list(map(list, product(coords2, coords1))))
        coords = np.concatenate([coords, np.zeros((coords.shape[0], 1))], axis=1)
        coords = coords[:, [0, 2, 1]]
        coords = self.rotate(coords, angle)
        output = list(map(lambda x: list(x) + [radius], coords))

        return np.array(output)
    
    # ------------------------- #

    def save(self, fname: str = 'particles.txt') -> None:

        path = os.path.join('../matlab', fname)

        with open(path, 'w') as f:
            for l in self.coords:
                f.write(','.join(map(str, l)) + '\n')

        f.close()

# ------------------------- #