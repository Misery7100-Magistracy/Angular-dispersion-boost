import numpy as np

# ------------------------- #

def resonance_m_squared(x, n):

    com = - 8*n**2*(n + 1) + (6*n + 3)*x**2 + 6*n
    denm = 2*n*x**2*(2*n - 1)
    sqrel = 4*n*(x**2)*(n - 3 + 4*n**2*(n + 2)) * (x**2 + 4*n - 2)
    
    res = - 1 / denm * (com + np.sqrt(sqrel + com ** 2))

    return res

# ------------------------- #