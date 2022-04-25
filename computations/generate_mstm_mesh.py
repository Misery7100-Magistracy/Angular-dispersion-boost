from processing import mis
import numpy as np
import yaml
import os

srcpath = os.path.realpath(__file__)
workdir, _ = os.path.split(srcpath)

# ------------------------- #

if __name__ == "__main__":

    with open(os.path.join(workdir, 'yml', 'meshgen.yml'), 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    radius = config['radius']
    k = 2 * np.pi / config['wavelength']
    x = k * radius
    
    m = mis.resonance_m_squared(x, n=1)

    if 1 - m > 10 / 1.3:
        m = mis.resonance_m_squared(x, n=2)

    m = np.sqrt(-m)

    mg = mis.MeshGenerator()
    mg.build_mesh(
        edge=config['edge'], 
        gap=config['gap'], 
        kind=config['kind'],
        radius=config['radius'],  
        m=m
    )

    fname = f"{config['kind']}_" + \
            f"{config['edge']}edge_" + \
            f"{config['gap']}gap_" + \
            f"{config['radius']}radius_" + \
            f"{config['nonregularity']}nonreg_" + \
            f"{m:.4f}m" + ".txt"

    mg.random_shift(max_shift=config['gap']*config['nonregularity'])
    mg.save(path=os.path.join(workdir, 'matlab', 'input', fname))
