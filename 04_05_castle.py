"""04_05_castle.py"""
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
        self.properties.setTitle('castle sample')
        self.properties.setSize(1200, 800)
        self.win.requestProperties(self.properties)
        self.setBackgroundColor(0, 0, 0)

        # マウス操作を禁止
        self.disableMouse()
        # カメラの設定
        self.camera.setPos(120, -120, 90)
        self.camera.lookAt(0, 0, 0)

        # 座標軸
        self.axis = self.loader.loadModel('models/zup-axis')
        self.axis.setPos(0, 0, 0)
        self.axis.setScale(1.5)
        self.axis.reparentTo(self.render)

        # グラウンド
        for i in range(128):
            for j in range(128):
                grass_block = self.loader.loadModel('models/grass_block')
                grass_block.setPos(i - 64, j - 64, -1)
                grass_block.reparentTo(self.render)

        # 壁
        for i in range(60):
            for j in range(40):
                for k in range(12):
                    if i == 0 or i == 59 or j == 0 or j == 39:
                        gold_block = self.loader.loadModel('models/gold_block')
                        gold_block.setPos(i - 30, j - 20, k)
                        gold_block.reparentTo(self.render)

        # 尖塔
        for x0, y0 in ((0, 0), (-30, -20), (-30, 20), (30, 20), (30, -20)):
            # シリンダー
            for i in range(13):
                for j in range(13):
                    for k in range(20):
                        if 5**2 < (i - 6)**2 + (j - 6)**2 <= 6**2:
                            bricks = self.loader.loadModel('models/bricks')
                            bricks.setPos(x0 + i - 6, y0 + j - 6, k)
                            bricks.reparentTo(self.render)

            # コーン（円錐）
            for i in range(13):
                for j in range(13):
                    for k in range(12):
                        r = 6 - k / 2
                        if ((r - 1) ** 2 < (i - 6) ** 2 + (j - 6) ** 2 <= r ** 2) or (i == 6 and j == 6 and k == 11):
                            blue_wool = self.loader.loadModel('models/blue_wool')
                            blue_wool.setPos(x0 + i - 6, y0 + j - 6, k + 20)
                            blue_wool.reparentTo(self.render)

            # サイン波
            for i in range(6):
                for j in range(3):
                    x = i
                    y = sin(pi * x / 6) * 2
                    z = j
                    red_wool = self.loader.loadModel('models/red_wool')
                    red_wool.setPos(x0 + x, y0 + y, z + 32)
                    red_wool.reparentTo(self.render)


app = App()
app.run()
