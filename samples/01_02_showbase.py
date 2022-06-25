"""Panda3D ShowBase"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *


class App(ShowBase):
    # コンストラクター
    def __init__(self):
        # 画面を生成する
        ShowBase.__init__(self)

        # ブロックを一つ置く
        cube = self.loader.loadModel('models/misc/rgbCube')
        cube.setPos(0, 10, 0)
        cube.reparentTo(self.render)


app = App()
app.run()
