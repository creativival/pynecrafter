"""src/block.py"""
import re
from math import *
from panda3d.core import *


class Block:

    def __init__(self, base, ground_size):
        self.base = base
        self.ground_size = ground_size
        self.block_dictionary = {}
        self.block_models = {}  # 追記
        # ブロックノード
        self.base.block_node = self.base.render.attachNewNode(PandaNode('block_node'))

        # グラウンドを作成
        self.set_flat_world()

    def add_block_dictionary(self, x, y, z, block_id):
        key = f'{floor(x)}_{floor(y)}_{floor(z)}'
        self.block_dictionary[key] = block_id

    def add_block_model(self, x, y, z, block_id):
        key = f'{floor(x)}_{floor(y)}_{floor(z)}'
        self.base.set(key, self.base.block_node.attachNewNode(PandaNode(key)))
        placeholder = self.base.get(key)
        placeholder.setPos(floor(x), floor(y), floor(z))
        # block = self.base.loader.loadModel(f'models/{block_id}')
        # block.reparentTo(placeholder)
        if block_id in self.block_models:
            block_model = self.block_models[block_id]
        else:
            block_model = self.base.loader.loadModel(f'models/{block_id}')
            self.block_models[block_id] = block_model
        block_model.instanceTo(placeholder)

    def add_block(self, x, y, z, block_id):
        self.add_block_dictionary(x, y, z, block_id)
        self.add_block_model(x, y, z, block_id)
        self.hide_invisible_blocks(Point3(x, y, z))

    def add_block_if_not_exists(self, x, y, z, block_id):
        if not self.is_block_at(Point3(x, y, z)):
            self.add_block(x, y, z, block_id)

    def remove_block_dictionary(self, x, y, z):
        key = f'{floor(x)}_{floor(y)}_{floor(z)}'
        if key in self.block_dictionary:
            del self.block_dictionary[key]

    def remove_block_model(self, x, y, z):
        key = f'{floor(x)}_{floor(y)}_{floor(z)}'
        placeholder = self.base.get(key)
        if placeholder:
            placeholder.removeNode()

    def remove_block(self, x, y, z):
        self.remove_block_dictionary(x, y, z)
        self.remove_block_model(x, y, z)
        self.hide_invisible_blocks(Point3(x, y, z))

    def set_flat_world(self):
        ground_size = self.ground_size
        # for i in range(ground_size):
        #     for j in range(ground_size):
        #         x = i - ground_size // 2
        #         y = j - ground_size // 2
        #         z = -1
        #         self.add_block(x, y, z, 'grass_block')
        ground_card = CardMaker("ground_card")
        ground_card.setFrame(
            -ground_size / 2,
            ground_size / 2,
            -ground_size / 2,
            ground_size / 2)
        ground_card.setUvRange(
            (0, 0),
            (ground_size, ground_size)
        )
        ground = self.base.render.attachNewNode(ground_card.generate())
        ground.setP(-90)
        ground.setZ(-0.01)
        grass_texture = self.base.loader.loadTexture("textures/0-0.png")
        ground.setTexture(grass_texture)

    def is_block_at(self, position):
        x, y, z = [floor(value) for value in position]
        key = f'{x}_{y}_{z}'
        return key in self.block_dictionary

    def can_add_or_remove_block_at(self, position):
        diff_positions = [
            Point3(1, 0, 0),
            Point3(0, 1, 0),
            Point3(0, 0, 1),
            Point3(-1, 0, 0),
            Point3(0, -1, 0),
            Point3(0, 0, -1),
        ]

        for diff_position in diff_positions:
            x, y, z = [floor(value) for value in position + diff_position]
            key = f'{x}_{y}_{z}'
            if key in self.block_dictionary or z == -1:
                return True
        else:
            return False

    def get_floor_height(self):
        x, y, z = [floor(value) for value in self.base.player.position]
        s = re.compile(f'{x}_{y}_.+')
        floor_height = -1
        for key in self.block_dictionary:
            if s.search(key):
                _, _, block_z = [int(value) for value in key.split('_')]
                if floor_height < block_z <= z:
                    floor_height = block_z
        return floor_height

    def hide_invisible_blocks(self, position):
        diff_positions = [
            Point3(1, 0, 0),
            Point3(0, 1, 0),
            Point3(0, 0, 1),
            Point3(-1, 0, 0),
            Point3(0, -1, 0),
            Point3(0, 0, -1),
        ]

        # 設置または削除したブロックの周辺ブロックをチェック（６ヶ所）
        # print('POSITION', position)
        for diff_position1 in diff_positions:
            block_position = position + diff_position1
            x, y, z = [floor(value) for value in block_position]
            key = f'{x}_{y}_{z}'
            placeholder = self.base.get(key)
            if placeholder:
                # 周辺ブロックが６つのブロックで囲まれているとき（見えないとき）、その周辺ブロックを隠す
                is_surrounded_by_six_blocks = True
                for diff_position2 in diff_positions:
                    check_position = block_position + diff_position2
                    if not self.is_block_at(check_position):
                        is_surrounded_by_six_blocks = False
                        break

                if is_surrounded_by_six_blocks:
                    if not placeholder.isHidden():
                        # print('hide', x, y, z)
                        placeholder.hide()
                else:
                    if placeholder.isHidden():
                        # print('show', x, y, z)
                        placeholder.show()
