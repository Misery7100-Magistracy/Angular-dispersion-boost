import numpy as np

# ------------------------- #

def read_bytes(fname, imsize):
    image = []

    with open(fname, 'rb') as f:
        while (byte := f.read(1)):
            image.append(int.from_bytes(byte, 'big'))
    
    f.close()
    image = np.array(image).reshape(imsize, imsize)

    return image