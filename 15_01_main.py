"""15_01_main.py"""
from math import *
from src import MC


class Game(MC):
    def __init__(self):
        # MCを継承する
        MC.__init__(self, ground_size=16, mode='debug')

        # 座標軸
        self.axis = self.loader.loadModel('models/zup-axis')
        self.axis.setPos(0, 0, 0)
        self.axis.setScale(1.5)
        self.axis.reparentTo(self.render)

        # 階段
        block_id = 'gold_block'
        for i in range(-7, 9):
            for j in range(-7, 9):
                for k in range(6):
                    if -2 <= j < 3:
                        if i < -2:
                            if k - i == 7:
                                self.block.add_block(i, j, k, block_id)
                        if -2 <= i < 3:
                            if k == 5:
                                self.block.add_block(i, j, k, block_id)
                        if 3 <= i:
                            if i + k == 7:
                                self.block.add_block(i, j, k, block_id)
                    if -2 <= i < 3:
                        if j < -2:
                            if k - j == 7:
                                self.block.add_block(i, j, k, block_id)
                        if -2 <= j < 3:
                            if k == 5:
                                self.block.add_block(i, j, k, block_id)
                        if 3 <= j:
                            if j + k == 7:
                                self.block.add_block(i, j, k, block_id)


game = Game()
game.run()
