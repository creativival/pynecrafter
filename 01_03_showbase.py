"""01_03_showbase.py"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *


class App(ShowBase):
    # コンストラクタ
    def __init__(self):
        # ShowBaseを継承する
        ShowBase.__init__(self)

        # ウインドウの設定
        self.properties = WindowProperties()
        self.properties.setTitle('Showbase sample')
        self.properties.setSize(1200, 800)
        self.win.requestProperties(self.properties)
        self.setBackgroundColor(0, 0, 0)

        # マウス操作を禁止
        self.disableMouse()
        # カメラの設定
        self.camera.setPos(5, 0, 10)
        self.camera.lookAt(0, 10, 0)

        # ブロックを一つ置く
        self.cube = self.loader.loadModel('models/misc/rgbCube')
        self.cube.setPos(0, 10, 0)
        self.cube.reparentTo(self.render)


app = App()
app.run()
