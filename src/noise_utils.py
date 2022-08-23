"""src/noise_utils.py"""
from noise import pnoise2, snoise2


def make_perlin_noise(wavelength=16, size=256):
    freq = 1 / wavelength
    return [[(snoise2(x * freq, y * freq) + 1) / 2 for x in range(size)] for y in range(size)]


if __name__ == '__main__':
    print(make_perlin_noise()[:1])
