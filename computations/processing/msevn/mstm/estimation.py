import numpy as np
from tqdm import tqdm
from scipy.io import loadmat
from itertools import product

# ------------------------- #

def thickness(edge = 15, gap = 166, radius = 20):
    return (edge - 1) * gap + 2 * radius

# ------------------------- #

def _calc_e_int(
    
        field, 
        idxs, 
        dphis: np.ndarray, # arrs args
        dthetas: np.ndarray, # arrs args
        coords: np.ndarray,
        thickness: float = thickness(),
        cylw: int = 400,
        mean_mode: bool = False

    ):

    x = coords[:, 0]
    y = coords[:, 1]
    z = coords[:, 2]

    globnrm = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    gl = np.where((globnrm >= 2 * thickness) & (globnrm <= (coords.max() * 1.02)))[0]

    x = x[gl]
    y = y[gl]
    z = z[gl]

    output = []

    for p in tqdm(dphis):

        row = []

        x1 = x * np.cos(np.pi * p / 180) - y * np.sin(np.pi * p / 180)
        y1 = x * np.sin(np.pi * p / 180) + y * np.cos(np.pi * p / 180)

        for t in dthetas:

            x2 = x1 * np.cos(np.pi * t / 180) + z * np.sin(np.pi * t / 180)
            y2 = y1
            z2 = z * np.cos(np.pi * t / 180) - x1 * np.sin(np.pi * t / 180)
            cylnrm = np.sqrt(x2 ** 2 + y2 ** 2)

            cylidx = np.where(cylnrm <= cylw)[0]
            cylzb0 = np.where(z2 >= 0)[0]

            stbl = list(set(cylidx).intersection(set(cylzb0)))
            stbl = gl[stbl]
            
            val = np.sum([field[idxs[i]] for i in stbl])

            if mean_mode and len(stbl) > 0:
                val /= len(stbl)

            row.append(val)
        
        output.append(row)
    
    return np.array(output).T # to plot as polar


# ------------------------- #

def e_int(

        matpath: str,
        dphi: np.ndarray,
        dtheta: np.ndarray,
        thickness: float,
        mean_mode: bool = False

    ):

    mat = loadmat(matpath)

    field = np.transpose(mat['eField3DAbs'], (1, 0, 2))
    field = field[::-1, :, :]
    #field = mat['eField3DAbs']
    field = np.nan_to_num(field)

    dim = field.shape[0]
    grid_max = int(mat['grid_max'][0][0])
    coord = np.linspace(-grid_max, grid_max, dim)

    idxs = list(product(range(dim), repeat=3))
    coords = np.array(list(product(coord, repeat=3)))

    result = _calc_e_int(
        field=field,
        idxs=idxs,
        coords=coords,
        thickness=thickness,
        dphis=dphi,
        dthetas=dtheta,
        mean_mode=mean_mode
    )

    return result

# ------------------------- #