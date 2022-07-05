"""06_01_main.py"""
from math import *
from src import MC


class Game(MC):
    def __init__(self):
        # MCを継承する
        MC.__init__(self)

        # 座標軸
        self.axis = self.loader.loadModel('models/zup-axis')
        self.axis.setPos(0, 0, 0)
        self.axis.setScale(1.5)
        self.axis.reparentTo(self.render)


game = Game()
game.run()
