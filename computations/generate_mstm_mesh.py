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
    
    m = mis.resonance_m_squared(config['radius'], n=1)

    if 1 - m > 4:
        m = mis.resonance_m_squared(config['radius'], n=2)

    m = np.sqrt(-m)

    mg = mis.MeshGenerator()
    mg.build_mesh(
        edge=config['edge'], 
        gap=config['gap'], 
        kind='cube',
        radius=config['radius'],  
        m=m
    )

    fname = f"{config['edge']}edge_" + \
            f"{config['gap']}gap_" + \
            f"{config['radius']}radius_" + \
            f"{config['nonregularity']}nonreg_" + \
            f"{m:.4f}m" + ".txt"

    mg.random_shift(max_shift=config['gap']*config['nonregularity'])
    mg.save(path=os.path.join(workdir, 'matlab', 'input', fname))
