"""src/utils.py"""
from direct.gui.DirectGui import OnscreenImage
from panda3d.core import TransparencyAttrib


class DrawImage(OnscreenImage):
    def __init__(self, image, parent, scale=(1, 1, 1), pos=(0, 0, 0)):
        super().__init__(image=image,
                         parent=parent,
                         pos=pos,
                         scale=scale,
                         )
        self.setName(image)
        self.setTransparency(TransparencyAttrib.M_alpha)
