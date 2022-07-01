"""04_04_sin_wave.py"""
from math import sin, pi
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *


class App(ShowBase):
    # コンストラクタ
    def __init__(self):
        # ShowBaseを継承する
        ShowBase.__init__(self)

        # ウインドウの設定
        self.properties = WindowProperties()
        self.properties.setTitle('sin_wave sample')
        self.properties.setSize(1200, 800)
        self.win.requestProperties(self.properties)
        self.setBackgroundColor(0, 0, 0)

        # マウス操作を禁止
        self.disableMouse()
        # カメラの設定
        self.camera.setPos(50, -50, 30)
        self.camera.lookAt(0, 0, 0)

        # 座標軸
        self.axis = self.loader.loadModel('models/zup-axis')
        self.axis.setPos(0, 0, 0)
        self.axis.setScale(1.5)
        self.axis.reparentTo(self.render)

        # グラウンド
        for i in range(64):
            for j in range(64):
                grass_block = self.loader.loadModel('models/grass_block')
                grass_block.setPos(i - 32, j - 32, -1)
                grass_block.reparentTo(self.render)

        # サイン波
        for i in range(64):
            for j in range(10):
                x = i - 32
                y = sin(pi * x / 32) * 5
                z = j
                red_wool = self.loader.loadModel('models/red_wool')
                red_wool.setPos(x, y, z)
                red_wool.reparentTo(self.render)


app = App()
app.run()
