"""src/player.py"""
from math import *
from panda3d.core import *
from direct.showbase.ShowBaseGlobal import globalClock
from .player_model import PlayerModel
from .camera import Camera


class Player(PlayerModel, Camera):
    heading_angular_velocity = 15000
    pitch_angular_velocity = 5000
    max_pitch_angle = 30
    speed = 10

    # コンストラクタ
    def __init__(self, base):
        PlayerModel.__init__(self, base)
        Camera.__init__(self, base)

        self.base = base
        self.position = Point3(0, 0, 0)
        self.direction = VBase3(0, 0, 0)
        self.velocity = Vec3(0, 0, 0)
        self.mouse_pos_x = 0
        self.mouse_pos_y = 0

        # キー操作を保存
        self.key_map = {
            'w': 0,
            'a': 0,
            's': 0,
            'd': 0,
        }

        # ユーザーのキー操作
        base.accept('w', self.update_key_map, ["w", 1])
        base.accept('a', self.update_key_map, ["a", 1])
        base.accept('s', self.update_key_map, ["s", 1])
        base.accept('d', self.update_key_map, ["d", 1])
        base.accept('w-up', self.update_key_map, ["w", 0])
        base.accept('a-up', self.update_key_map, ["a", 0])
        base.accept('s-up', self.update_key_map, ["s", 0])
        base.accept('d-up', self.update_key_map, ["d", 0])

        # プレイヤーのアップデート
        base.taskMgr.add(self.player_update, "player_update")

    def update_direction(self):
        if self.base.mouseWatcherNode.hasMouse():
            dt = globalClock.getDt()
            x, y = self.base.mouseWatcherNode.getMouse()
            dx = x - self.mouse_pos_x
            dy = y - self.mouse_pos_y
            heading = self.direction.x
            pitch = self.direction.y
            heading -= dx * Player.heading_angular_velocity * dt
            pitch += dy * Player.pitch_angular_velocity * dt
            if pitch < -Player.max_pitch_angle:
                pitch = -Player.max_pitch_angle
            elif pitch > Player.max_pitch_angle:
                pitch = Player.max_pitch_angle
            self.direction = VBase3(heading, pitch, 0)
            self.mouse_pos_x = x
            self.mouse_pos_y = y

    def update_key_map(self, key_name, key_state):
        self.key_map[key_name] = key_state

    def update_velocity(self):
        key_map = self.key_map

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
        self.base.player_node.setH(self.direction.x)
        self.base.player_head_node.setP(self.direction.y)
        self.base.player_node.setPos(self.position)

    def player_update(self, task):
        self.update_direction()
        self.update_position()
        self.draw()
        return task.cont
