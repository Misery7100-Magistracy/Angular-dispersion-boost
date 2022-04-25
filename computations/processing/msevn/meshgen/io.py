

def save(data, path: str = 'particles.txt') -> None:
    with open(path, 'w') as f:
        for l in data:
            f.write(','.join(map(str, l)) + '\n')

    f.close()