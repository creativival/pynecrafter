"""src/architecture.py"""
from math import *
from random import randint
from panda3d.core import *


class Architecture:

    def make_road(self, length=128, width=9, initial_position=Point3(0, 0, 0), angle=0):
        for i in range(length):
            for j in range(width):
                if 0 < i % 10 < 5 and j == width // 2:
                    block_id = 'sand'
                else:
                    block_id = 'stone'
                for k in [0, 0.5]:
                    x = (i + k) * cos(radians(angle)) - (j + k) * sin(radians(angle))
                    y = (i + k) * sin(radians(angle)) + (j + k) * cos(radians(angle))
                    z = -1
                    position = initial_position + Point3(x, y, z)
                    self.block.add_block_if_not_exists(*position, block_id)

    def make_tree(self, initial_position=Point3(0, 0, 0), log_block_id='oak_log'):
        x, y, z = initial_position
        tree_height = randint(6, 8)
        leaf_block_id = 'oak_leaves'
        for i in range(tree_height):
            if i < 3:
                self.block.add_block_if_not_exists(x, y, z + i, log_block_id)
            elif i == tree_height - 1:
                self.block.add_block_if_not_exists(x, y, z + i, leaf_block_id)
            else:
                for j in range(3):
                    for k in range(3):
                        self.block.add_block_if_not_exists(x - 1 + j, y - 1 + k, z + i, leaf_block_id)

    def make_house(self, initial_position=Point3(0, 0, 0), w=10, d=12, h=12,
              roof_block_id='red_wool', wall_block_id='white_wool', pillar_block_id='brown_wool'):
        x, y, z = initial_position
        half_w = int((w + 2) / 2)
        # 屋根の高さを計算する
        heights = []
        for i in range(w + 2):
            if i < half_w:
                if w % 2 == 0:
                    heights.append(h - half_w + i)
                else:
                    heights.append(h - half_w + i - 1)
            else:
                heights.append(h + half_w - i - 1)
        print(heights)

        # 家を建築する
        for i in range(w + 2):
            for j in range(d):
                roof_height = heights[i]
                if 0 < i < w + 1:  # 家の部分
                    for k in range(roof_height):
                        if (i == 1 or i == w) or (j == 0 or j == d - 1):  # 壁の部分
                            if (i == 1 and j == 0) or (i == 1 and j == d - 1) or \
                                    (i == w and j == 0) or (i == w and j == d - 1):  # 四隅の柱部分
                                block_id = pillar_block_id
                            elif heights[i] >= h - 1 and (k == 3 or k == 4):  # 窓部分
                                block_id = 'glass'
                            else:
                                block_id = wall_block_id
                            self.block.add_block_if_not_exists(i + x, j + y, k + z, block_id)
                    else:
                        self.block.add_block_if_not_exists(i + x, j + y, k + z + 1, roof_block_id)
                else:  # 屋根の張り出し部分
                    self.block.add_block_if_not_exists(i + x, j + y, heights[1] + z - 1, roof_block_id)
