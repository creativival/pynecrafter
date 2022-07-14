"""src/utils.py"""
from direct.gui.DirectGui import OnscreenImage, OnscreenText
from panda3d.core import *


class DrawImage(OnscreenImage):
    def __init__(self, image, parent, scale=(1, 1, 1), pos=(0, 0, 0)):
        super().__init__(image=image,
                         parent=parent,
                         pos=pos,
                         scale=scale,
                         )
        self.setName(image)
        self.setTransparency(TransparencyAttrib.M_alpha)


class DrawText(OnscreenText):
    def __init__(self, text, parent, font, scale=0.07, pos=(0.05, -0.1), fg=(0, 0, 0, 1), bg=(0, 0, 0, 0.1)):
        super().__init__(text=text,
                         parent=parent,
                         align=TextNode.ALeft,
                         pos=pos,
                         scale=scale,
                         font=font,
                         fg=fg,
                         bg=bg,
                         mayChange=True,
                         )
        self.start_time = None
