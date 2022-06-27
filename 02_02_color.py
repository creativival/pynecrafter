"""02_02_color.py"""
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
        self.camera.setPos(0, -50, 0)
        self.camera.lookAt(0, 0, 0)

        # ブロックを置く
        for i in range(20):
            for j in range(20):
                cube = self.loader.loadModel('models/misc/rgbCube')
                cube.setPos(i - 10, 0, j - 10)
                # ２色の合成
                # cube.setColor(j / 20, i / 20, 0)
                # cube.setColor(0, j / 20, i / 20)
                # cube.setColor(i / 20, 0, j / 20)
                # 3色の合成
                cube.setColor(j / 20, i / 20, 1)
                # cube.setColor(1, j / 20, i / 20)
                # cube.setColor(i / 20, 1, j / 20)
                cube.reparentTo(self.render)


app = App()
app.run()
