"""src/user_interface.py"""
from math import *
from panda3d.core import *
from .draw_image import DrawImage


class UserInterface:
    hotbar_blocks = [
        ['stone', ['0-1']],
        ['grass_block', ['0-3', '0-0', '0-2']],
        ['dirt', ['0-2']],
        ['white_wool', ['4-0']],
        ['blue_wool', ['11-1']],
        ['red_wool', ['8-1']],
        ['glass', ['3-1']],
        ['gold_block', ['1-7']],
        # ['diamond_block', ['1-8']],
        # ['emerald_block', ['1-9']],
        ['bricks', ['0-7']],
    ]

    def __init__(self):
        self.selected_hotbar_num = 0
        self.selected_block = UserInterface.hotbar_blocks[0]

        # draw hotbar
        for i, block in enumerate(UserInterface.hotbar_blocks):
            block_image_name = block[1][0]
            image = DrawImage(
                f'textures/{block_image_name}.png',
                self.a2dpBottomCenter,
                scale=(16 / 164, 16 / 164, 16 / 164),
                pos=((i - 4) * 0.22, 0, 20 / 164)
            )
            self.set(f'bar{i + 1}', image)
        self.hotbar = DrawImage(
            'images/hotbar1.png',
            self.a2dpBottomCenter,
            scale=(1, 1, 20 / 164),
            pos=(0, 0, 20 / 164)
        )

        # select item
        for i in range(1, 10):
            self.accept(str(i), self.select, [i])

    def select(self, i):
        self.selected_hotbar_num = i - 1
        self.selected_block = UserInterface.hotbar_blocks[i - 1]
        self.hotbar.setImage(f'images/hotbar{i}.png')
        self.hotbar.setTransparency(TransparencyAttrib.M_alpha)


