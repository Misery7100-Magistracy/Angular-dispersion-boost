import wave
import numpy as np
import os
from itertools import product
from ..mie.equations import resonance_m_squared
from ..mie.constants import *

# ------------------------- #

def build(

        node_radius : float = 20., # in nanometers
        d_relative: float = 2,
        wavelength: float = 83, # in nanometers
        edgecount: int = 16

    ):

    gap = d_relative * wavelength
    rng = node_radius + gap * (edgecount - 1) / 2

    x = np.linspace(-rng, rng, edgecount)
    xyz = np.array(list(map(list, product(x, repeat=3))))

    ka = node_radius * 2 * np.pi / wavelength

    flag = True
    order = 1

    while flag:

        m = resonance_m_squared(ka, n=order)

        if 1 - m <= SOLID_LIMIT:
            flag = False
        
        else:
            order += 1
    
    m_im = np.sqrt(-m)



    
    output = list(map(lambda x: list(x) + [node_radius, 0, m_im], xyz))

    return output

# ------------------------- #