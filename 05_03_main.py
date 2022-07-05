"""05_03_main.py"""
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

        # お城
        # 壁
        for i in range(60):
            if i % 3 == 0:
                for y in (-20, -17, 16, 19):
                    self.block.add_block(i - 30, y, 16, 'diamond_block')
                if i < 40:
                    for x in [-30, -25, 25, 29]:
                        self.block.add_block(x, i - 20, 16, 'diamond_block')
            for j in range(40):
                for k in range(16):
                    if 0 <= i <= 3 or 56 <= i <= 59 or 0 <= j <= 3 or 36 <= j <= 39:
                        self.block.add_block(i - 30, j - 20, k, 'gold_block')

        # 台座
        for i in range(18):
            for j in range(14):
                for k in range(12):
                    self.block.add_block(i - 9, j - 7, k, 'emerald_block')

        # 尖塔
        for x0, y0 in ((0, 0), (-28, -18), (-28, 18), (28, 18), (28, -18)):
            if x0 == 0:
                shift_z = 12
            else:
                shift_z = 0
            for i in range(13):
                for j in range(13):
                    # シリンダー
                    for k in range(20):
                        if 5 ** 2 < (i - 6) ** 2 + (j - 6) ** 2 <= 6 ** 2:
                            self.block.add_block(x0 + i - 6, y0 + j - 6, k + shift_z, 'bricks')

                    # コーン（円錐）
                    for k in range(12):
                        r = 6 - k / 2
                        if ((r - 1) ** 2 < (i - 6) ** 2 + (j - 6) ** 2 <= r ** 2) or (i == 6 and j == 6 and k == 11):
                            self.block.add_block(x0 + i - 6, y0 + j - 6, k + 20 + shift_z, 'blue_wool')

            # サイン波
            for i in range(6):
                for j in range(3):
                    x = i
                    y = sin(pi * x / 6) * 2
                    z = j
                    self.block.add_block(x0 + x, y0 + y, z + 32 + shift_z, 'red_wool')

        # 大門
        for i in range(6):
            for j in range(40):
                for k in range(9):
                    self.block.remove_block(i - 3, j - 20, k)

        # 尖塔の窓
        for x0, y0 in ((0, 0), (-28, -18), (-28, 18), (28, 18), (28, -18)):
            if x0 == 0:
                shift_z = 12
            else:
                shift_z = 0
            for i in range(80):
                for j in range(1, 4):
                    h = j * 5
                    self.block.remove_block(x0, y0 + i - 40, h + shift_z)
                    self.block.remove_block(x0, y0 + i - 40, h + shift_z + 1)
                    self.block.remove_block(x0 + i - 40, y0, h + shift_z)
                    self.block.remove_block(x0 + i - 40, y0, h + shift_z + 1)


game = Game()
game.run()
