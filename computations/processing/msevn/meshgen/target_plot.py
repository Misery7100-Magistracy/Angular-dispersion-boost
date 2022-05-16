import numpy as np
from itertools import product

# ------------------------- #

def rotate(data, a=0) -> np.ndarray:

    a = -a

    return data.dot(np.array([

            [np.cos(a), 0, np.sin(a)],
            [0, 1, 0],
            [-np.sin(a), 0, np.cos(a)]
            
        ]))

# ------------------------- #

def project_2d(

        radius=20.,
        gap=10.,
        edge=10.,
        mult=4,
        angle=0,
        thin=True

    ) -> np.ndarray:

    angle *= (np.pi / 180)

    rng = radius + gap * (edge - 1) / 2
    coords1 = np.linspace(-rng, rng, edge)
    coords2 = np.linspace(-rng*mult, rng*mult, edge*mult)
    coords = np.array(list(map(list, product(coords2, coords1))))
    coords = np.concatenate([coords, np.zeros((coords.shape[0], 1))], axis=1)
    coords = coords[:, [0, 2, 1]]

    if thin: 
        
        coords = np.array(list(filter(lambda x: abs(x[2]) == rng, coords)))
    
    #print(coords)

    coords = rotate(coords, angle)
    output = list(map(lambda x: list(x) + [radius], coords))

    return np.array(output)

# ------------------------- #