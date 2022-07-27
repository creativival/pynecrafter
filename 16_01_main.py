"""16_01_main.py"""
from math import *
from panda3d.core import *
from src import MC


class Game(MC):
    def __init__(self):
        # MCを継承する
        MC.__init__(self, ground_size=256, mode='debug')

        # プレイヤーの位置を変更
        self.player.position = Point3(0, -30, 0)

        # 座標軸
        self.axis = self.loader.loadModel('models/zup-axis')
        self.axis.setPos(0, 0, 0)
        self.axis.setScale(1.5)
        self.axis.reparentTo(self.render)

        # # 箱
        # for i in range(3):
        #     for j in range(3):
        #         for k in range(3):
        #             self.block.add_block(i, j, k, 'gold_block')

        # ドーム
        radius = 20
        block_id = 'gold_block'
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                for k in range(radius + 1):
                    if i**2 + j**2 + k**2 <= radius**2:
                        self.block.add_block(i, j, k, block_id)


game = Game()
game.run()
