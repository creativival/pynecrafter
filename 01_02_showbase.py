"""01_02_showbase.py"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *


class App(ShowBase):
    # コンストラクタ
    def __init__(self):
        # ShowBaseを継承する
        ShowBase.__init__(self)

        # ブロックを一つ置く
        self.cube = self.loader.loadModel('models/misc/rgbCube')
        self.cube.setPos(0, 10, 0)
        self.cube.reparentTo(self.render)


app = App()
app.run()
