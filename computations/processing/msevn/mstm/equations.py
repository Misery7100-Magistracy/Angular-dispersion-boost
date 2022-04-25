import numpy as np

# ------------------------- #

def miller_h(t, p, drel, phi0, theta0):

    fterm = np.cos(np.pi / 180 * theta0) * np.sin(np.pi / 180 * t) * np.cos(np.pi / 180 * (p - phi0))

    sterm = np.sin(np.pi / 180 * theta0) * (np.cos(np.pi / 180 * t) - 1)

    return drel * (fterm - sterm)

# ------------------------- #

def miller_l(t, p, drel, theta0):

    fterm = np.sin(np.pi / 180 * theta0) * np.sin(np.pi / 180 * t) * np.cos(np.pi / 180 * p)

    sterm = np.cos(np.pi / 180 * theta0) * (np.cos(np.pi / 180 * t) - 1)

    return drel * (fterm + sterm)

# ------------------------- #

def miller_k(t, p, drel, phi0):

    return drel * np.sin(np.pi / 180 * t) * np.sin(np.pi / 180 * (p - phi0))

# ------------------------- #