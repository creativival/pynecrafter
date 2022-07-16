"""src/utils.py"""
from direct.gui.DirectGui import OnscreenImage, OnscreenText, DirectButton
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


class DrawMenuButton(DirectButton):
    def __init__(self, base, text, parent, pos, command):
        super().__init__(
            geom=(
                base.button_model.find('**/button_up'), base.button_model.find('**/button_press'),
                base.button_model.find('**/button_over'), base.button_model.find('**/button_disabled')
            ),
            text=text,
            parent=parent,
            pos=pos,
            command=command,
            scale=0.5,
            text_fg=(1, 1, 1, 1),
            text_scale=0.1,
            text_pos=(0, -0.04),
            text_font=base.font,
            relief=None,
        )
