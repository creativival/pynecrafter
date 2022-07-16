"""src/menu.py"""
from panda3d.core import *
from direct.gui.DirectGui import *
from .utils import *


class Menu:
    def __init__(self):
        self.font = self.loader.loadFont('fonts/PixelMplus12-Regular.ttf')
        self.menu_node = self.aspect2d.attachNewNode('menu_node')
        self.menu_node.stash()
        self.save_node = self.aspect2d.attachNewNode('save_node')
        self.save_node.stash()
        self.load_node = self.aspect2d.attachNewNode('load_node')
        self.load_node.stash()

        menu_cm = CardMaker('menu_card')
        menu_cm.setFrame(-1.5, 1.5, -1, 1)
        self.menu_background_node = self.render2d.attachNewNode(menu_cm.generate())
        self.menu_background_node.setTransparency(1)
        self.menu_background_node.setColor(0, 0, 0, 0.5)
        self.menu_background_node.stash()

        self.button_model = self.loader.loadModel('models/button_maps')

        # Pause Screen
        self.unpause_button = self.draw_menu_button('Resume Game', self.menu_node, (0, 0, 0.4), self.toggle_menu)
        self.save_button = self.draw_menu_button('Save Game', self.menu_node, (0, 0, 0.24), self.toggle_save)
        self.load_button = self.draw_menu_button('Load Game', self.menu_node, (0, 0, 0.08), self.toggle_load)
        self.server_button = self.draw_menu_button('Open server', self.menu_node, (0, 0, -0.08), self.toggle_menu)
        self.join_button = self.draw_menu_button('Join Server', self.menu_node, (0, 0, -0.24), self.join_server)
        self.exit_button = self.draw_menu_button('Quit Game', self.menu_node, (0, 0, -0.4), exit)

        self.accept('q', self.toggle_menu)

    def draw_menu_button(self, text, parent, pos, command):
        return DirectButton(
            geom=(
                self.button_model.find('**/button_up'), self.button_model.find('**/button_press'),
                self.button_model.find('**/button_over'), self.button_model.find('**/button_disabled')
            ),
            text=text,
            parent=parent,
            pos=pos,
            command=command,
            scale=0.5,
            text_fg=(1, 1, 1, 1),
            text_scale=0.1,
            text_pos=(0, -0.04),
            text_font=self.font,
            relief=None,
        )

    def toggle_menu(self):
        if self.menu_node.isStashed():
            self.menu_node.unstash()
            self.menu_background_node.unstash()
        else:
            self.menu_node.stash()
            self.menu_background_node.stash()
            
    def toggle_save(self):
        if self.menu_node.isStashed():
            self.menu_node.stash()
            self.menu_node.unstash()
        else:
            self.menu_node.unstash()
            self.menu_node.stash()
            
    def toggle_load(self):
        if self.load_node.isStashed():
            self.menu_node.stash()
            self.load_node.unstash()
        else:
            self.menu_node.unstash()
            self.load_node.stash()
            
    def open_server(self):
        pass
            
    def join_server(self):
        pass

