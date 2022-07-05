"""src/player.py"""
from math import *
from panda3d.core import *
from direct.showbase.ShowBaseGlobal import globalClock


class Player:
    heading_angular_velocity = 200
    pitch_angular_velocity = 75
    max_pitch_angle = 30
    speed = 10

    # コンストラクタ
    def __init__(self, base):
        self.base = base
        self.position = Point3(0, 0, 0)
        self.direction = VBase3(0, 0, 0)
        self.velocity = Vec3(0, 0, 0)

        self.player_node = self.base.render.attachNewNode(PandaNode('player_node'))
        self.player_model = self.base.loader.loadModel('models/panda')
        self.player_model.setH(180)
        self.player_model.reparentTo(self.player_node)
        # self.player_axis = self.base.loader.loadModel('models/zup-axis')
        # self.player_axis.setScale(3)
        # self.player_axis.reparentTo(self.player_node)

        # キー操作を保存
        self.key_map = {
            'w': 0,
            'a': 0,
            's': 0,
            'd': 0,
        }

        # ユーザーのキー操作
        self.base.accept('w', self.update_key_map, ["w", 1])
        self.base.accept('a', self.update_key_map, ["a", 1])
        self.base.accept('s', self.update_key_map, ["s", 1])
        self.base.accept('d', self.update_key_map, ["d", 1])
        self.base.accept('w-up', self.update_key_map, ["w", 0])
        self.base.accept('a-up', self.update_key_map, ["a", 0])
        self.base.accept('s-up', self.update_key_map, ["s", 0])
        self.base.accept('d-up', self.update_key_map, ["d", 0])

        # プレイヤーのアップデート
        self.base.taskMgr.add(self.player_update, "player_update")

    def update_direction(self):
        if self.base.mouseWatcherNode.hasMouse():
            dt = globalClock.getDt()
            mouse_pos = self.base.mouseWatcherNode.getMouse()
            x = mouse_pos.x
            y = mouse_pos.y
            print(x, y)
            heading = self.direction.x
            pitch = self.direction.y
            if x < -0.05 or 0.05 < x:
                heading -= x * Player.heading_angular_velocity * dt
            if y < -0.05 or 0.05 < y:
                pitch -= y * Player.pitch_angular_velocity * dt
            if pitch < -Player.max_pitch_angle:
                pitch = -Player.max_pitch_angle
            elif pitch > Player.max_pitch_angle:
                pitch = Player.max_pitch_angle
            self.direction = VBase3(heading, pitch, 0)

    def update_key_map(self, key_name, key_state):
        self.key_map[key_name] = key_state

    def update_velocity(self):
        key_map = self.key_map
        print(key_map)

        if key_map['w'] or key_map['a'] or key_map['s'] or key_map['d']:
            heading = self.direction.x
            if key_map['w'] and key_map['a']:
                angle = 135
            elif key_map['a'] and key_map['s']:
                angle = 225
            elif key_map['s'] and key_map['d']:
                angle = 315
            elif key_map['d'] and key_map['w']:
                angle = 45
            elif key_map['w']:
                angle = 90
            elif key_map['a']:
                angle = 180
            elif key_map['s']:
                angle = 270
            else:  # key_map['d']
                angle = 0
            self.velocity = \
                Vec3(
                    cos(radians(angle + heading)),
                    sin(radians(angle + heading)),
                    0
                ) * Player.speed
        else:
            self.velocity = Vec3(0, 0, 0)

    def update_position(self):
        self.update_velocity()
        dt = globalClock.getDt()
        self.position = self.position + self.velocity * dt
        # print(self.position)

    def draw(self):
        self.player_node.setH(self.direction.x)
        self.player_node.setP(self.direction.y)
        self.player_node.setPos(self.position)

    def player_update(self, task):
        self.update_direction()
        self.update_position()
        self.draw()
        return task.cont
