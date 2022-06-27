"""02_01_coordinate.py"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *


class App(ShowBase):
    # コンストラクタ
    def __init__(self):
        # ShowBaseを継承する
        ShowBase.__init__(self)

        # ウインドウの設定
        self.properties = WindowProperties()
        self.properties.setTitle('Color sample')
        self.properties.setSize(1200, 800)
        self.win.requestProperties(self.properties)
        self.setBackgroundColor(0, 0, 0)

        # マウス操作を禁止
        self.disableMouse()
        # カメラの設定
        self.camera.setPos(40, -50, 50)
        self.camera.lookAt(0, 0, 0)

        # 座標軸
        self.axis = self.loader.loadModel('models/zup-axis')
        self.axis.setPos(0, 0, 0)
        self.axis.setScale(1.5)
        self.axis.reparentTo(self.render)

        # ブロックを置く
        self.cube1 = self.loader.loadModel('models/misc/rgbCube')
        self.cube1.setPos(10, 0, 0)
        self.cube1.reparentTo(self.render)

        self.cube2 = self.loader.loadModel('models/misc/rgbCube')
        self.cube2.setPos(0, 10, 0)
        self.cube2.reparentTo(self.render)

        self.cube3 = self.loader.loadModel('models/misc/rgbCube')
        self.cube3.setPos(10, 10, 0)
        self.cube3.reparentTo(self.render)

        self.cube4 = self.loader.loadModel('models/misc/rgbCube')
        self.cube4.setPos(10, 10, 10)
        self.cube4.reparentTo(self.render)


app = App()
app.run()
