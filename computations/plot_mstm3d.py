from scipy.io import loadmat
from itertools import product
import os

from processing import mis
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker
from tqdm.autonotebook import tqdm

srcpath = os.path.realpath(__file__)
workdir, _ = os.path.split(srcpath)

mis.configure_mpl()

# ------------------------- #

def thickness(edge = 15, gap = 166, radius = 20):
    return (edge - 1) * gap + 2 * radius

def E_int_opt(
    
        field, 
        idxs, 
        dphis, # arrs args
        dthetas, # arrs args
        coords,
        thickness = thickness(gap = 249),
        cylw = 400

    ):

    x = coords[:, 0]
    y = coords[:, 1]
    z = coords[:, 2]

    globnrm = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    gl = np.where(globnrm > 2 * thickness)[0]

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
            row.append(val)
        
        output.append(row)
    
    return np.array(output).T # to plot as polar


# ------------------------- #

root = '../matlab/output'

#file = loadmat(os.path.join(root, '15edge_166gap_8.9radius_0.0nonreg_1.8502m_14.78deg_TEpol_83wav_800bw.mat'))
file = loadmat(os.path.join(root, '15edge_249gap_20radius_0.0nonreg_1.8667m_14.78deg_TEpol_83wav_800bw.mat'))

field = np.transpose(file['eField3DAbs'], (1, 0, 2))
field = np.nan_to_num(field)

dim = field.shape[0]
grid_max = int(file['grid_max'][0][0])
coord = np.linspace(-grid_max, grid_max, dim)

idxs = list(product(range(dim), repeat=3))
coords = np.array(list(product(coord, repeat=3)))

dphis = np.linspace(0, 180, 40)
dthetas = np.linspace(0, 90, 50)

eintcalc = E_int_opt(dphis=dphis, dthetas=dthetas, coords=coords, field=field, idxs=idxs)


dphimesh, dthetamesh = np.meshgrid(np.append(dphis, dphis + 180) * np.pi / 180, dthetas) #rectangular plot of polar data

# plotting

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, polar='True')
ax.grid(True, alpha=0.2, color='black')
cax = ax.contourf(dphimesh, dthetamesh, np.concatenate([eintcalc, eintcalc[:, ::-1]], axis=1), cmap='turbo', levels=np.linspace(0, eintcalc.max(), 100), zorder=-1)
ax.set_xlabel(r'$\Delta \varphi$', labelpad=15)
ax.set_xticklabels([r'$' + str(i) + r'^{\circ}$' for i in range(0, 360, 45)])
ax.set_rgrids(range(20, 90, 20), angle=0)
ax.xaxis.set_tick_params(pad=10)

cbar = plt.colorbar(cax, fraction=0.046, pad=0.1)
cbar.set_label(r'$E_{\rm{int}}$', labelpad=15)
ax.set_rmax(90)

cbar.ax.yaxis.set_major_locator(ticker.LinearLocator(8))

rlab = ax.set_ylabel(r'$\Delta \theta$')
rlab.set_position((5, 0.44))
rlab.set_rotation(0)
ax.yaxis.labelpad = -350