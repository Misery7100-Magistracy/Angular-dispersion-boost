import numpy as np
from .io import read_bytes
import os

# ------------------------- #

def __find_htr_row(row, shift: int = 10, nm_per_pixel: float = 0.1, low_thresh: int = 15):
    length = len(row)
    max_val = np.mean(row[length // 2 - shift: length // 2 + shift])
    min_val = low_thresh

    idx2 = set(np.where(row > min_val)[0])
    idx3 = set(np.where(row < max_val*0.7)[0])
    idx = idx3.intersection(idx2)

    thkns = len(idx) * nm_per_pixel

    return thkns

# ------------------------- #

def __find_core_row(row, shift: int = 10, nm_per_pixel: float = 0.1, max_thresh: float = 225):
    length = len(row)

    idx2 = set(np.where(row >= max_thresh)[0])

    core = len(idx2) * nm_per_pixel

    return core

# ------------------------- #

def __find_htr(arr, shift: int = 10, nm_per_pixel: float = 0.1):
        
    thkns = np.mean([__find_htr_row(k, shift=shift, nm_per_pixel=nm_per_pixel) for k in arr[:len(arr) // 2]])
    return thkns

# ------------------------- #

def __find_core(arr, nm_per_pixel: float = 0.1, max_thresh: float = 225):
        
    cores = np.mean([__find_core_row(k, nm_per_pixel=nm_per_pixel, max_thresh=max_thresh) for k in arr[:len(arr) // 2]])
    return cores

# ------------------------- #

def thickness_transition_layer(
    
        datadir: str, 
        imagesize: int = 1600, 
        nm_per_pixel: float = 250 / 1600 # nm per image pixel
    
    ):

    postdir = os.path.join(datadir, 'Post')
    density_el = read_bytes(os.path.join(postdir, 'spacetime-de'), imagesize)
    thickness = __find_htr(density_el, nm_per_pixel=nm_per_pixel)

    return thickness

# ------------------------- #

def thickness_core(
    
        datadir: str, 
        imagesize: int = 1600, 
        nm_per_pixel: float = 250 / 1600, # nm per image pixel
        max_thresh: float = 225
    
    ):

    postdir = os.path.join(datadir, 'Post')
    density_el = read_bytes(os.path.join(postdir, 'spacetime-de'), imagesize)
    cres = __find_core(density_el, nm_per_pixel=nm_per_pixel, max_thresh=max_thresh)

    return cres

# ------------------------- #