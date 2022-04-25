import os
import yaml

# ------------------------- #

def read_config(config: str) -> dict:
    with open(os.path.relpath(config), 'r') as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    
    return conf

# ------------------------- #

srcpath = os.path.realpath(__file__)
workdir, _ = os.path.split(srcpath)
cfgpath = os.path.join(workdir, 'plotting.yml')

plot_config = read_config(cfgpath)