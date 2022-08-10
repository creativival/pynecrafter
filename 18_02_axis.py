"""18_02_axis.py"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *


class App(ShowBase):
    # コンストラクタ
    def __init__(self):
        # ShowBaseを継承する
        ShowBase.__init__(self)

        # カメラ
        self.disableMouse()
        self.camera.setPos(0, -60, 10)
        self.camera.lookAt(0, 30, 0)

        # 座標軸
        self.axis = self.loader.loadModel('models/zup-axis')
        self.axis.setPos(3, 0, 0)
        self.axis.setScale(1.5)
        self.axis.reparentTo(self.render)

        self.mcpi_world = self.render.attachNewNode(PandaNode('mcpi_world'))
        self.mcpi_world.setPos(-3, 0, 0)
        self.mcpi_world.setHpr(180, 90, 0)

        self.axis = self.loader.loadModel('models/zup-axis')
        self.axis.setPos(0, 0, 0)
        self.axis.setScale(1.5)
        self.axis.reparentTo(self.mcpi_world)



app = App()
app.run()
