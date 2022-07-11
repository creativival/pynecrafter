""" render
Minecraft Clone
"""
import sqlite3
import os

from math import floor
from time import time
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.actor.Actor import Actor
from src.network import Server, Client, ServerProtocol, ClientProtocol
from direct.distributed.PyDatagram import PyDatagram
from src.architecture import Architecture
from src.block import Block
from src.dummy_block import DummyBlock
from src.draw_image import DrawImage
from src.draw_text import DrawText
from src.inventory import Inventory
from src.menu import Menu
from src.mob import Mob
from src.player import Player
from src.turtle import Turtle
from src.i18n import I18n
from src.utils import *

title = 'PandaCraft3D'
settings = {
    # 'default_font': "fonts/Minecraftia.ttf",
    # 'default_font': "fonts/Meiryo.ttf",
    # 'default_font': "fonts/PixelMplus10-Regular.ttf",
    'default_font': "fonts/PixelMplus12-Regular.ttf",
    'near_far': (0.18, 500),
    # 'screen_size': (1200, 800),
    'screen_size': (1280, 720),
    'fullscreen': False,
    'background_color': (0, 1, 1),
    # 'world_size': (257, 257, 128),
    'max_length_to_add_block': 7,
    'bgm': 'music/BitCastle.mp3',
    'action_sound': 'music/minecraft_action.mp3',
    'gravity_force': 9.8,
    'player_move_speed': 10,
    'player_jump_speed': 10,
    'mob_jump_speed': 5,
    'color_variation': [
        VBase3(255, 165, 204),  # pink
        VBase3(255, 199, 38),  # yellow
        VBase3(255, 52, 36),  # red
        VBase3(128, 255, 37),  # green
        VBase3(160, 212, 255),  # skyblue
        VBase3(255, 255, 255),  # white
        VBase3(254, 159, 159),  # lightpink
        VBase3(42, 43, 79),  # darkblue
    ],
    'mob': {
        'box': {'size': 1},
        'camera': {'size': 1},
        'cmr12': {'size': 1},
        'cmss12': {'size': 1},
        'cmtt12': {'size': 1},
        'environment': {'size': 1},
        'frog': {'size': 0.3},
        'frowney': {'size': 1},
        'jack': {'size': 1},
        'panda': {'size': 1},
        'panda-model': {'size': 0.01},
        'panda-walk': {'size': 1},
        'panda-walk4': {'size': 0.01},
        'pig': {'size': 0.3},
        'piyo': {'size': 0.3},
        'ripple': {'size': 1},
        'smiley': {'size': 1},
        'teapot': {'size': 1},
    },
}


class Minecraft(ShowBase):
    def __init__(self, ground_size=(-64, 64), player_position=None, mob_nums={}, locale='en', debug=False):
        ShowBase.__init__(self)

        # settings
        self.ground_size = ground_size
        self.settings = settings
        self.mob_nums = mob_nums
        self.debug = debug

        # translate
        self.i18n = I18n('translate', locale)
        # print(self.i18n.t('HowToUse'))

        # splash screen
        self.splash_screen_node = self.aspect2d.attachNewNode("inventory_screen")
        self.splash_image = DrawImage(
            'images/splash_screen.png',
            self.splash_screen_node,
            scale=(9 / 6, 1, 1),
            pos=(0, 0, 0),
        )
        self.loading_text = DrawText(self,
                                     'creating a new world...',
                                     parent=self.splash_screen_node,
                                     pos=(-.2, -.5, 0),
                                     scale=0.1,
                                     fg=(0, 0, 0, 1))
        self.graphicsEngine.renderFrame()
        self.graphicsEngine.renderFrame()
        self.splash_screen_node.stash()

        # window setting
        self.props = WindowProperties()
        self.props.setTitle(title)
        self.props.setSize(*self.settings['screen_size'])
        self.props.setFullscreen(self.settings['fullscreen'])
        self.win.requestProperties(self.props)
        self.setBackgroundColor(*self.settings['background_color'])

        # camera setting
        self.camLens.setNearFar(*self.settings['near_far'])  # 遠方は表示しない（デフォルトは100000）

        # mouse setting
        self.disableMouse()
        props = WindowProperties()
        # props.setCursorHidden(True)
        # props.setMouseMode(WindowProperties.M_relative)
        self.win.requestProperties(props)

        # sqlite3
        dest = f'saves/worlds.db'
        dest_dir = os.path.dirname(dest)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        self.db = sqlite3.connect(dest)
        cursor = self.db.cursor()
        args = ("current",)
        cursor.execute("select name from sqlite_master where name=?", args)

        if len(cursor.fetchall()) > 0:
            cursor.execute("delete from current")
        else:
            cursor.execute(
                "create table current ("
                "x integer, "
                "y integer, "
                "z integer, "
                "block_id text"
                ")")
        self.db.commit()
        cursor.close()

        # ground
        self.ground_card = CardMaker("plane")
        self.make_ground()

        # block
        self.block_node = self.render.attachNewNode(PandaNode('block_node'))
        self.block = Block(self)
        self.block_changes = []  # for multiplayer mode to sync blocks

        # turtle
        self.turtle = Turtle(self.block)

        # architecture
        self.architecture = Architecture(self.block)

        # draw text
        self.has_text_window = True
        how_to_use = self.i18n.t('HowToUse')
        # how_to_use = ''
        self.text_window = DrawText(self, how_to_use, scale=0.05, fg=(0, 0, 0, 1))
        wellcome_text = self.i18n.t('Wellcome to Panda3DCraft!')
        self.console_window = DrawText(self, wellcome_text, fg=(0, 0, 0, 1), pos=(0.05, -1.5))
        self.console_window.start_time = time()

        # player
        self.player_node = self.render.attachNewNode(PandaNode('player_node'))
        self.player = Player(self, player_position)
        # self.player_node.stash()

        # dummy block
        self.dummy_block = DummyBlock(self)

        # draw hotbar
        for i, block_id in enumerate(self.block.hotbar_block_ids):
            image = DrawImage(
                f'cube_textures/{block_id}.png',
                self.a2dpBottomCenter,
                scale=(16 / 164, 16 / 164, 16 / 164),
                pos=((i - 4) * 0.22, 0, 20 / 164)
            )
            self.set(f'bar{i + 1}', image)
        self.hotbar = DrawImage(
            'images/hotbar.png',
            self.a2dpBottomCenter,
            scale=(1, 1, 20 / 164),
            pos=(0, 0, 20 / 164)
        )

        # draw inventory
        self.has_inventory_screen = False
        self.inventory = Inventory(self)

        # draw menu
        self.has_menu_screen = False
        self.menu = Menu(self)

        # draw background
        self.has_background_screen = False
        cm = CardMaker('card')
        self.background = self.render2d.attachNewNode(cm.generate())
        self.background.setPos(-1, 0, -1)
        self.background.setScale(2)
        self.background.setTransparency(1)
        self.background.setColor(0, 0, 0, 0.5)
        self.background.hide()

        # Allow playing two music files at the same time.
        self.musicManager.setConcurrentSoundLimit(2)

        # bgm
        self.bgm = self.loader.loadMusic(self.settings['bgm'])
        self.bgm.setLoop(True)
        self.bgm.play()

        # action sound
        self.action_sound = self.loader.loadMusic(self.settings['action_sound'])

        # mob
        self.mob_node = self.render.attachNewNode(PandaNode('mob_node'))
        self.mob_distance_list = []
        self.mobs = []
        self.mob_models = {}
        for mob_name, data in self.settings['mob'].items():
            if mob_name == 'panda-walk':
                model = Actor("panda", {"walk": mob_name})
                model.loop("walk")
            elif mob_name == 'panda-walk4':
                model = Actor("panda-model", {"walk": mob_name})
                model.loop("walk")
            else:
                model = self.loader.loadModel(f'mob_models/{mob_name}.bam')
            size = data['size']
            model.setScale(size)
            self.mob_models[mob_name] = model
        # print(self.mob_models)
        for mob_name, j in self.mob_nums.items():
            for i in range(j):
                self.mobs.append(
                    Mob(self, mob_name, i)
                )

        # multiplayer
        self.multiplayer = None
        self.guest_player_node = self.render.attachNewNode(PandaNode('guest_player_node'))
        self.guest_player = None

        # point light
        plight = PointLight('plight')
        plight.setColor((0.2, 0.2, 0.2, 1))
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(10, 20, 0)
        self.render.setLight(plnp)

        # # directional light
        # dlight = DirectionalLight('dlight')
        # dlight.setColor((0.8, 0.8, 0.5, 1))
        # dlnp = self.render.attachNewNode(dlight)
        # dlnp.setHpr(0, -60, 0)
        # self.render.setLight(dlnp)

        # ambient light
        alight = AmbientLight('alight')
        alight.setColor((1, 1, 1, 0.5))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        # key_map
        self.key_map = {
            "w": False,
            "a": False,
            "s": False,
            "d": False,
            "arrow_up": False,
            "arrow_down": False,
            "space": False,
            "mouse1": False,
            "mouse3": False,
        }

        # control a player with key
        self.accept('w', self.update_key_map, ["w", True])
        self.accept('a', self.update_key_map, ["a", True])
        self.accept('s', self.update_key_map, ["s", True])
        self.accept('d', self.update_key_map, ["d", True])
        self.accept('arrow_up', self.update_key_map, ["arrow_up", True])
        self.accept('arrow_down', self.update_key_map, ["arrow_down", True])
        self.accept("space", self.update_key_map, ["space", True])
        self.accept('mouse1', self.update_key_map, ["mouse1", True])
        self.accept('mouse3', self.update_key_map, ["mouse3", True])
        self.accept('w-up', self.update_key_map, ["w", False])
        self.accept('a-up', self.update_key_map, ["a", False])
        self.accept('s-up', self.update_key_map, ["s", False])
        self.accept('d-up', self.update_key_map, ["d", False])
        self.accept('arrow_up-up', self.update_key_map, ["arrow_up", False])
        self.accept('arrow_down-up', self.update_key_map, ["arrow_down", False])
        self.accept("space-up", self.update_key_map, ["space", False])
        self.accept('mouse1-up', self.update_key_map, ["mouse1", False])
        self.accept('mouse3-up', self.update_key_map, ["mouse3", False])
        # self.accept('mouse1', self.block.player_remove_block)
        # self.accept('mouse3', self.block.player_add_block)
        self.accept('t', self.toggle_cam)
        # show
        self.accept('e', self.show_inventory)
        self.accept('escape', self.show_menu)
        self.accept('f', self.fix_camera)
        # select item
        for i in range(1, 10):
            self.accept(str(i), self.select, [i])
        # chat
        self.accept('h', self.hello_func)
        self.accept('j', self.thank_you_func)
        # text window
        self.accept('x', self.toggle_text_window)
        # # server
        self.accept('o', self.open_server)
        self.accept('c', self.connect_as_a_client)
        # change ground size
        self.accept('g', self.change_ground_size, [(0, 100)])

        # move the player
        self.taskMgr.add(self.player.update, "player_update")

        # move mob
        self.taskMgr.add(self.mob_update, "mob_update")

        # dummy_block
        self.taskMgr.add(self.dummy_block.update, "dummy_block_update")

        # screen
        self.taskMgr.add(self.screen_update, "screen_update")

    def update_key_map(self, key_name, key_state):
        self.key_map[key_name] = key_state

    def screen_update(self, task):
        if self.debug:
            position = self.player.position
            direction = self.player.direction
            velocity = self.player.velocity
            text = f'player x: {round(position[0], 1)}\n' \
                   f'player y: {round(position[1], 1)}\n' \
                   f'player z: {round(position[2], 1)}\n' \
                   f'player heading: {int(direction[0])}\n' \
                   f'player pitch: {int(direction[1])}\n' \
                   f'player roll: {int(direction[2])}\n' \
                   f'player velocity x: {round(velocity[0], 1)}\n' \
                   f'player velocity y: {round(velocity[1], 1)}\n' \
                   f'player velocity z: {round(velocity[2], 1)}\n' \
                   f'player fly height: {self.player.fly_height}\n' \
                   f'player jump state: {self.player.jump_status}\n'
            self.text_window.setText(text)
        # 3秒でコンソールの文字を消す
        if self.console_window.getText() and time() - self.console_window.start_time > 3:
            self.console_window.setText('')
        return task.cont

    def mob_update(self, task):
        self.mob_distance_list = distance_list_of_vectors(
            [mob.position for mob in self.mobs]
        )
        # print(self.mob_distance_list)
        for mob in self.mobs:
            mob.update()
        return task.cont

    def toggle_cam(self):
        self.player.toggle_cam()

    def select(self, i):
        self.block.selected_bar_num = i
        self.block.selected_block_id = self.block.hotbar_block_ids[i - 1]
        self.hotbar.setImage(f'images/hotbar{i}.png')
        self.hotbar.setTransparency(TransparencyAttrib.M_alpha)

    def show_inventory(self):
        if not (self.has_menu_screen or self.has_background_screen):
            if self.has_inventory_screen:
                self.inventory.hide()
                self.has_inventory_screen = False
            else:
                self.inventory.show()
                self.has_inventory_screen = True

    def show_menu(self):
        if not (self.has_inventory_screen or self.has_background_screen):
            if self.has_menu_screen:
                self.menu.hide()
                self.has_menu_screen = False
            else:
                self.menu.show()
                self.has_menu_screen = True

    def fix_camera(self):
        if not (self.has_inventory_screen or self.has_menu_screen):
            if self.has_background_screen:
                self.background.hide()
                self.has_background_screen = False
            else:
                self.background.show()
                self.has_background_screen = True
                self.console_window.setText(self.i18n.t('Fix camera'))
                self.console_window.start_time = time()

    def toggle_text_window(self):
        if self.has_text_window:
            self.text_window.hide()
            self.has_text_window = False
        else:
            self.text_window.show()
            self.has_text_window = True

    def open_server(self):
        self.menu.change_button_to_disable()
        self.console_window.setText(self.i18n.t('Open server'))
        self.console_window.start_time = time()
        self.guest_player = Player(self, (0, 0, 0), is_guest=True)
        # サーバーを立ち上げて、spriteの速度と位置を送信
        # guest_spriteの速度と位置を受信
        # guest_spriteの速度を変更する
        self.multiplayer = Server(self, ServerProtocol(self), 9999)

        # move guest player
        self.taskMgr.add(self.guest_player.update, "guest_player_update")

    def connect_as_a_client(self):
        self.menu.change_button_to_disable()
        self.console_window.setText(self.i18n.t('Connect as a client'))
        self.console_window.start_time = time()
        self.guest_player = Player(self, (0, 0, 0), is_guest=True)
        # クライエントを立ち上げて、guest_spriteの速度と位置を受信
        # guest_spriteの速度を変更する
        # spriteの速度と位置を送信
        self.multiplayer = Client(self, ClientProtocol(self))
        self.multiplayer.connect("localhost", 9999, 3000)

        # move guest player
        self.taskMgr.add(self.guest_player.update, "guest_player_update")

    def hello_func(self):
        data = PyDatagram()
        data.addUint8(10)
        data.addString("Hello!")
        if self.multiplayer:
            if self.multiplayer.network_state == 'server':
                self.multiplayer.broadcast(data)
            else:
                self.multiplayer.send(data)

    def thank_you_func(self):
        data = PyDatagram()
        data.addUint8(10)
        data.addString("Thank you!")
        if self.multiplayer:
            if self.multiplayer.network_state == 'server':
                self.multiplayer.broadcast(data)
            else:
                self.multiplayer.send(data)

    def clear_world(self):
        print('block and mob clear')
        # block
        self.block_node.removeNode()
        self.block_node = self.render.attachNewNode(PandaNode('block_node'))
        cursor = self.db.cursor()
        cursor.execute("delete from current")
        self.db.commit()
        cursor.close()
        # mob
        self.mob_node.removeNode()
        self.mob_node = self.render.attachNewNode(PandaNode('mob_node'))
        self.mobs = []

    def get(self, var):
        try:
            return getattr(self, var)
        except AttributeError:
            return None

    def set(self, var, val):
        setattr(self, var, val)

    def change_ground_size(self, new_ground_size):
        self.plane.removeNode()
        # self.ground_card.clearSourceGeometry()
        # self.ground_card.reset()
        self.ground_size = new_ground_size
        self.make_ground()

    def make_ground(self):
        size = self.ground_size
        self.ground_card.setFrame(size[0], size[1], size[0], size[1])
        self.ground_card.setUvRange(
            (0, 0),
            (size[1] - size[0], size[1] - size[0])
        )
        self.plane = self.render.attachNewNode(self.ground_card.generate())
        self.plane.setP(-90.)
        self.plane.setZ(-0.01)
        road_tex = self.loader.loadTexture("cube_textures/grass_block_top.png")
        self.plane.setTexture(road_tex)

    def load_object(self, obj):
        x, y, z, object_id = obj
        # print(x, y, z, object_id)
        if 'ground_size' in object_id:
            x, y, z = int(x), int(y), int(z)
            self.change_ground_size((x, y))
        elif 'player' in object_id:
            if self.multiplayer:
                player = self.guest_player
            else:
                player = self.player
            x, y, z = float(x), float(y), float(z)
            player.position = Point3(x, y, z)
        elif object_id.split('_')[0] in self.settings['mob'].keys():
            mob_name, mob_id, color_id = object_id.split('_')
            x, y, z = float(x), float(y), float(z)
            self.mobs.append(
                Mob(self, mob_name, int(mob_id), color_id, position=(x, y, z))
            )
        elif object_id in self.block.all_block_ids:
            x, y, z = int(x), int(y), int(z)
            cursor = self.db.cursor()
            args = (x, y, z, object_id)
            cursor.execute("insert into current(x,y,z,block_id) values(?,?,?,?)", args)
            self.db.commit()
            cursor.close()

    def can_go_there(self, x1, y1, z1, x2, y2, z2):
        x1, y1, z1 = floor(x1), floor(y1), floor(z1)
        x2, y2, z2 = floor(x2), floor(y2), floor(z2)
        cursor = self.db.cursor()
        args = [x2, y2, z2, x2, y2, z2 + 1]
        if y1 < y2:
            args[1] += 1
            args[4] += 1
        if x1 < x2:
            args[0] += 1
            args[3] += 1
        cursor.execute("select count(*) from current where "
                       "(x=? and y=? and z=?) or "
                       "(x=? and y=? and z=?)"
                       "", args)
        count = cursor.fetchone()[0]
        cursor.close()
        # print(not count)
        return not count
