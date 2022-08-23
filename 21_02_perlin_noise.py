"""21_02_perlin_noise.py"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from src import *


class PerlinNoise(ShowBase):
    WAVELENGTH = 16
    SIZE = 256
    MIN_RATE = 0.8

    # コンストラクタ
    def __init__(self):
        # ShowBaseを継承する
        ShowBase.__init__(self)

        # ウインドウの設定
        self.properties = WindowProperties()
        self.properties.setTitle('Perlin noise sample')
        self.properties.setSize(1200, 800)
        self.win.requestProperties(self.properties)
        self.setBackgroundColor(0, 0, 0)

        # マウス操作を禁止
        self.disableMouse()
        # カメラの設定
        self.camera.setPos(0, -PerlinNoise.SIZE * 1.1, PerlinNoise.SIZE * 1.1)
        self.camera.lookAt(0, 0, 0)

        perlin_noise = make_perlin_noise(wavelength=PerlinNoise.WAVELENGTH, size=PerlinNoise.SIZE)

        # ブロックを置く
        for i in range(PerlinNoise.SIZE):
            for j in range(PerlinNoise.SIZE):
                noise = perlin_noise[j][i]
                if noise > PerlinNoise.MIN_RATE:
                    cube = self.loader.loadModel('models/misc/rgbCube')
                    cube.setPos(i - PerlinNoise.SIZE / 2, j - PerlinNoise.SIZE / 2, 0)
                    cube.setColor(noise, noise, noise)
                    cube.reparentTo(self.render)


perlin_noise = PerlinNoise()
perlin_noise.run()
