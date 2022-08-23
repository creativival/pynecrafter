"""src/mc.py"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from . import *


class MC(ShowBase, UserInterface, Inventory, Menu, Architecture, ConnectToMCPI,
         Sound, Cloud):
    def __init__(self, ground_size=128, mode='normal', cloud_range=0):
        self.mode = mode
        self.ground_size = ground_size
        self.enable_sound_effect = False
        # ShowBaseを継承する
        ShowBase.__init__(self)
        self.font = self.loader.loadFont('fonts/PixelMplus12-Regular.ttf')
        UserInterface.__init__(self)
        Inventory.__init__(self)
        Menu.__init__(self)
        if self.mode == 'mcpi':
            ConnectToMCPI.__init__(self)
        Sound.__init__(self)
        if cloud_range:
            Cloud.__init__(self, cloud_range)

        # ウインドウの設定
        self.properties = WindowProperties()
        self.properties.setTitle('Pynecrafter')
        self.properties.setSize(1200, 800)
        self.properties.setSize(960, 540)  # TODO
        self.win.requestProperties(self.properties)
        self.setBackgroundColor(0, 1, 1)

        # ブロック
        self.block = Block(self, ground_size)

        # プレイヤー
        self.player = Player(self)

        # ゲーム終了
        self.accept('escape', self.exit_game)

    def exit_game(self):
        if self.db:
            self.cursor.close()
            self.db.close()
        exit()

    def get(self, var):
        try:
            return getattr(self, var)
        except AttributeError:
            return None

    def set(self, var, val):
        setattr(self, var, val)
