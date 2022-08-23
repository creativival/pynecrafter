from noise import pnoise2, snoise2


def make_perlin_noise(octaves=1, size=256):
    wavelength = 16.0 * octaves
    freq = 1 / wavelength
    perlin_noise = []
    for y in range(size):
        tmp_list = []
        for x in range(size):
            tmp_list.append(int(snoise2(x * freq, y * freq, octaves) * (size / 2 - 1.0) + size / 2))
        perlin_noise.append(tmp_list)
    print(perlin_noise)
    return perlin_noise


if __name__ == '__main__':
    make_perlin_noise()
