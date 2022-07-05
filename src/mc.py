"""src/mc.py"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from . import *


class MC(ShowBase):
    def __init__(self, ground_size=128):
        # ShowBaseを継承する
        ShowBase.__init__(self)

        # ウインドウの設定
        self.properties = WindowProperties()
        self.properties.setTitle('Pynecrafter')
        self.properties.setSize(1200, 800)
        self.win.requestProperties(self.properties)
        self.setBackgroundColor(0, 1, 1)

        # マウス操作を禁止
        self.disableMouse()
        # カメラの設定
        self.camera.setPos(60, -150, 90)
        self.camera.lookAt(0, 0, 0)

        # ブロック
        self.block = Block(self, ground_size)

    def get(self, var):
        try:
            return getattr(self, var)
        except AttributeError:
            return None

    def set(self, var, val):
        setattr(self, var, val)
