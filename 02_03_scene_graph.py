"""02_03_scene_graph.py"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *


class App(ShowBase):
    # コンストラクタ
    def __init__(self):
        # ShowBaseを継承する
        ShowBase.__init__(self)

        # ウインドウの設定
        self.properties = WindowProperties()
        self.properties.setTitle('Scene Graph sample')
        self.properties.setSize(1200, 800)
        self.win.requestProperties(self.properties)
        self.setBackgroundColor(0, 0, 0)

        # マウス操作を禁止
        self.disableMouse()
        # カメラの設定
        self.camera.setPos(0, -50, 0)
        self.camera.lookAt(0, 0, 0)

        # シーングラフ
        self.scene_node = self.render.attachNewNode(PandaNode('scene_node'))

        # ブロックを置く
        for i in range(20):
            cube = self.loader.loadModel('models/misc/rgbCube')
            cube.setPos(i - 10, 0, 0)
            cube.setColor(i / 20, 0, 1)
            if i < 10:
                cube.reparentTo(self.render)
            else:
                cube.reparentTo(self.scene_node)

        # scene_nodeを斜め上に移動
        self.scene_node.setPos(-1, 0, 1)

        # 色を赤にして、階段上に並べる
        for i, child in enumerate(self.scene_node.getChildren()):
            child.setColor(1, 0, 0)
            child.setZ(child.getZ() + i)


app = App()
app.run()
