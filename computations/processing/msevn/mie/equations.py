import scipy.special as scs
import numpy as np
import math

# ------------------------- #

def a_n_sph0(x, n, m):
    
    z1 = 1
    z2 = 2 * np.math.factorial(2*n - 1) * np.math.factorial(2*n + 1) / (4 ** n * np.math.factorial(n + 1) * np.math.factorial(n))
    z2 *= ((m ** 2 + (1 + n) / n) / (m ** 2 - 1))
    z2 /= (x ** (2 * n + 1))
    
    return np.vectorize(complex)(z1, z2) ** (-1)

# ------------------------- #

def a_n_sph1(x, n, m):
    
    z1 = 1
    z2 = 2 ** (1 + 2*n) * x ** (- 1 - 2*n)
    z2 *= 4 * (1 + n + m**2 * n) * (-3 + 4*n*(1 + n)) - \
    2 * (m**2 - 1) * (3 + n * (5 + 2*n + m**2 * (2*n - 1))) * x**2
    z2 *= math.gamma(n - 1/2) * math.gamma(n + 5/2)
    z2 /= ((m**2 - 1) * np.pi * (4 * (1 + n) * (3 + 2*n) **2 - \
        2 * (m**2 + 1) * (1 + n) * (3 + 2*n) * x**2))
    
    return np.vectorize(complex)(z1, z2) ** (-1)

# ------------------------- #

def a_n_sph_full(x, n, m):
    
    sp_jn_x = scs.spherical_jn(n, x)
    sp_jn_xd = scs.spherical_jn(n, x, True)
    
    sp_yn_x = scs.spherical_yn(n, x)
    sp_yn_xd = scs.spherical_yn(n, x, True)
    sp_h1_x = np.vectorize(complex)(sp_jn_x, sp_yn_x)
    sp_h1_xd = np.vectorize(complex)(sp_jn_xd, sp_yn_xd)
    
    sp_jn_mx = scs.spherical_jn(n, m*x)
    sp_jn_mxd = scs.spherical_jn(n, m*x, True)
    
    z11 = m**2 * sp_jn_mx * (x * sp_jn_xd + sp_jn_x)
    z12 = sp_jn_x * (m*x * sp_jn_mxd + sp_jn_mx)
    z21 = m**2 * sp_jn_mx * (x * sp_h1_xd + sp_h1_x)
    z22 = sp_h1_x * (m*x * sp_jn_mxd + sp_jn_mx)

    return (z11 - z12) / (z21 - z22)

# ------------------------- #

def eps_drude(nenc, beta=0):
    
    ee = 1 - nenc  / np.vectorize(complex)(1, beta)
    
    return ee ** 0.5

# ------------------------- #

@np.vectorize
def resonance_m_squared(x, n):
    
    com = - 8*n**2*(n + 1) + (6*n + 3)*x**2 + 6*n
    denm = 2*n*x**2*(2*n - 1)

    sqrel = 4*n*(x**2)*(n - 3 + 4*n**2*(n + 2)) * (x**2 + 4*n - 2)

    res = - 1 / denm * (com + np.sqrt(sqrel + com ** 2))
    
    return res

# ------------------------- #