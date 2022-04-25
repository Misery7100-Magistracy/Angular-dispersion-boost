from processing.msevn import mesh_generator
import yaml
import os

srcpath = os.path.realpath(__file__)
workdir, _ = os.path.split(srcpath)

# ------------------------- #

if __name__ == "__main__":

    with open(os.path.join(workdir, 'yml', 'meshconfig.yml'), 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    prms = dict(
        node_radius=config['radius'],
        d_relative=config['d_relative'],
        wavelength=config['wavelength'],
        edgecount=config['edge']
    )

    delta_d_max = config['nonregularity'] * prms['d_relative'] * prms['wavelength']

    if config['kind'] == 'cubic':
        mesh = mesh_generator.cubic.build(**prms)
    
    elif config['kind'] == 'cylinder':
        mesh = mesh_generator.cylinder.build(**prms)

    fname = f"{config['kind']}_" + \
            f"{config['edge']}edge_" + \
            f"{config['d_relative']}d_relative_" + \
            f"{config['wavelength']}wlen_" + \
            f"{config['radius']}radius_" + \
            f"{config['nonregularity']}nonreg.txt"
    
    mesh = mesh_generator.irreg.apply(mesh, delta_d_max)
    mesh_generator.save(mesh, path=os.path.join(workdir, 'matlab', 'input', fname))

# ------------------------- #