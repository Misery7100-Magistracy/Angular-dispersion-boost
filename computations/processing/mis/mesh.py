import numpy as np
import os
from itertools import product
from typing import Any, List, Dict

# ------------------------- #

class MeshGenerator:

    def __init__(self) -> None:

        self.coords = list()
    
    # ......................... #

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

    def random_shift(self, max_shift: float) -> None:
        
        for k in range(len(self.data)):
            xyz = self.data[k][:3]
            dist = np.random.uniform(low=0, high=max_shift)
            self.data[k][:3] = self.gen_with_predef_dist(xyz, dist)
        
        print('modified!')

    # ------------------------- #

    @staticmethod
    def gen_with_predef_dist(a, dist) -> List[List[float]]:

        x_shift = np.random.uniform(-dist, dist)
        dist = np.sqrt(dist ** 2 - x_shift ** 2)
        y_shift = np.random.uniform(-dist, dist)
        dist = np.sqrt(dist ** 2 - y_shift ** 2)
        z_shift = dist * np.random.choice([-1, 1])

        shifts = [x_shift, y_shift, z_shift]
        np.random.shuffle(shifts)

        return [a[i] + shifts[i] for i in range(len(a))]

    # ......................... #

    @staticmethod
    def rotate(data, a=0) -> np.ndarray:

        return data.dot(np.array([

                [np.cos(a), 0, np.sin(a)],
                [0, 1, 0],
                [-np.sin(a), 0, np.cos(a)]
                
            ]))

    # ......................... #

    def project_2d(

            self,
            radius=20.,
            gap=10.,
            edge=10.,
            mult=4,
            angle=0,
            thin=True

        ) -> np.ndarray:

        angle *= (np.pi / 180)

        rng = (2*radius + gap) * (edge - 1) / 2
        coords1 = np.linspace(-rng, rng, edge)
        coords2 = np.linspace(-rng*mult, rng*mult, edge*mult)
        coords = np.array(list(map(list, product(coords2, coords1))))
        coords = np.concatenate([coords, np.zeros((coords.shape[0], 1))], axis=1)
        coords = coords[:, [0, 2, 1]]

        if thin: 
            
            coords = np.array(list(filter(lambda x: abs(x[2]) == rng, coords)))
        
        #print(coords)

        coords = self.rotate(coords, angle)
        output = list(map(lambda x: list(x) + [radius], coords))

        return np.array(output)
    
    # ......................... #

    def save(self, fname: str = 'particles.txt') -> None:

        path = os.path.join('../matlab', fname)

        with open(path, 'w') as f:
            for l in self.data:
                f.write(','.join(map(str, l)) + '\n')

        f.close()

# ------------------------- #