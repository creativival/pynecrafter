"""18_01_main.py"""
from math import *
from random import randint, choice
from panda3d.core import *
from src import MC


class Game(MC):
    def __init__(self):
        # MCを継承する
        MC.__init__(self, ground_size=256, mode='mcpi')

        # プレイヤーの位置を変更
        self.player.position = Point3(5, -30, 0)

        # 座標軸
        self.axis = self.loader.loadModel('models/zup-axis')
        self.axis.setPos(0, 0, 0)
        self.axis.setScale(1.5)
        self.axis.reparentTo(self.render)

        # 壁
        for i in range(4):
            for j in range(3):
                if i == 0:
                    self.block.add_block(i, 0, j, 'stone')
                else:
                    self.block.add_block(i, 0, j, 'gold_block')

        # 道路
        self.make_road(initial_position=Point3(-64, 0, 0))
        self.make_road(length=64, initial_position=Point3(9, -32, 0), angle=90)
        self.make_road(length=32, initial_position=Point3(9, 30, 0), angle=45)
        self.make_road(length=32, initial_position=Point3(9, 35, 0), angle=135)

        # 街路樹
        for i in range(-101, 100, 10):
            for j in [-1, 9]:
                self.make_tree(initial_position=Point3(i, j, 0))

        # 家
        count = 0
        roof_colors = ['red', 'blue', 'green', 'pink', 'gray']
        for i in range(-51, 40, 30):
            for j in [-21, 30]:
                w = randint(8, 10)
                d = randint(8, 10)
                h = randint(8, 10)
                x = i + (21 - w) // 2
                if j == -21:
                    y = j
                else:
                    y = j - d
                # roof_block_id = choice(roof_colors) + '_wool'
                roof_block_id = roof_colors[count % len(roof_colors)] + '_wool'
                self.make_house(initial_position=Point3(x, y, 0), w=w, d=d, h=h, roof_block_id=roof_block_id)
                count += 1


game = Game()
game.run()
