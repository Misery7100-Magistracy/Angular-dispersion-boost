import numpy as np

# ------------------------- #

def __gen_with_predef_dist(a, dist) -> list:

        x_shift = np.random.uniform(-dist, dist)
        dist = np.sqrt(dist ** 2 - x_shift ** 2)
        y_shift = np.random.uniform(-dist, dist)
        dist = np.sqrt(dist ** 2 - y_shift ** 2)
        z_shift = dist * np.random.choice([-1, 1])

        shifts = [x_shift, y_shift, z_shift]
        np.random.shuffle(shifts)

        return [a[i] + shifts[i] for i in range(len(a))]

# ------------------------- #

def apply(data, max_shift: float) -> None:
    
    for k in range(len(data)):
        xyz = data[k][:3]
        dist = np.random.uniform(low=0, high=max_shift)
        data[k][:3] = __gen_with_predef_dist(xyz, dist)
    
    return data

# ------------------------- #