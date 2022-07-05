"""05_explanation1.py"""
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
        self.properties.setTitle('block settings')
        self.properties.setSize(1200, 800)
        self.win.requestProperties(self.properties)
        self.setBackgroundColor(0, 1, 1)

        # マウス操作を禁止
        self.disableMouse()
        # カメラの設定
        self.camera.setPos(10, -15, 1)
        self.camera.lookAt(0, 0, 0)

        # グラウンド
        for i in range(128):
            for j in range(128):
                grass_block = self.loader.loadModel('models/grass_block')
                grass_block.setPos(i - 64, j - 64, -1)
                grass_block.reparentTo(self.render)

        # 壁
        for i in range(2):
            for j in range(2):
                gold_block = self.loader.loadModel('models/gold_block')
                gold_block.setPos(i, 0, j)
                gold_block.reparentTo(self.render)

        positions = [
            (-1, 0, 1, 'stone'),
            (-2, 0, 1, 'stone'),
            (2, 0, 2, 'bricks'),
            (4, 0, 1, 'bricks'),
        ]

        for x, y, z, block_id in positions:
            gold_block = self.loader.loadModel(f'models/{block_id}')
            gold_block.setPos(x, y, z)
            gold_block.reparentTo(self.render)


app = App()
app.run()
