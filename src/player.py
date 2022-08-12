"""src/player.py"""
from math import *
from panda3d.core import *
from direct.showbase.ShowBaseGlobal import globalClock
from .player_model import PlayerModel
from .camera import Camera
from .target import Target


class Player(PlayerModel, Camera, Target):
    heading_angular_velocity = 15000
    pitch_angular_velocity = 5000
    max_pitch_angle = 60
    speed = 10
    eye_height = 1.6
    gravity_force = 9.8
    jump_speed = 10

    # コンストラクタ
    def __init__(self, base):
        self.base = base
        PlayerModel.__init__(self)
        Camera.__init__(self)
        Target.__init__(self)

        self.position = Point3(0, 0, 0)
        self.direction = VBase3(0, 0, 0)
        self.velocity = Vec3(0, 0, 0)
        self.mouse_pos_x = 0
        self.mouse_pos_y = 0
        self.target_position = None
        self.is_on_ground = True  # 地面に接している
        self.is_flying = False  # 空中に浮かんでいる
        self.is_walking = False  # 歩いている
        self.walking_count = 0  # 歩行のカウント
        # self.passed_time_of_jump = None
        # self.jump_positions_with_time = None

        # キー操作を保存
        self.key_map = {
            'w': 0,
            'a': 0,
            's': 0,
            'd': 0,
            'space': 0,
            'arrow_up': 0,
            'arrow_down': 0,
        }

        # ユーザーのキー操作
        base.accept('w', self.update_key_map, ["w", 1])
        base.accept('w-up', self.update_key_map, ["w", 0])
        base.accept('a', self.update_key_map, ["a", 1])
        base.accept('a-up', self.update_key_map, ["a", 0])
        base.accept('s', self.update_key_map, ["s", 1])
        base.accept('s-up', self.update_key_map, ["s", 0])
        base.accept('d', self.update_key_map, ["d", 1])
        base.accept('d-up', self.update_key_map, ["d", 0])
        base.accept('mouse1', self.player_remove_block)
        base.accept('mouse3', self.player_add_block)
        base.accept('space', self.update_key_map, ["space", 1])
        base.accept('space-up', self.update_key_map, ["space", 0])
        base.accept('arrow_up', self.update_key_map, ["arrow_up", 1])
        base.accept('arrow_up-up', self.update_key_map, ["arrow_up", 0])
        base.accept('arrow_down', self.update_key_map, ["arrow_down", 1])
        base.accept('arrow_down-up', self.update_key_map, ["arrow_down", 0])

        # プレイヤーのアップデート
        base.taskMgr.add(self.player_update, "player_update")
        base.taskMgr.doMethodLater(0.5, self.update_motion, "update_motion")

    def update_direction(self):
        if self.base.mouseWatcherNode.hasMouse() and \
                self.base.inventory_node.isStashed() and \
                self.base.menu_background_node.isStashed():
            dt = globalClock.getDt()
            x, y = self.base.mouseWatcherNode.getMouse()
            dx = x - self.mouse_pos_x
            dy = y - self.mouse_pos_y
            if dx or dy:
                heading = self.direction.x - dx * Player.heading_angular_velocity * dt
                pitch = self.direction.y + dy * Player.pitch_angular_velocity * dt
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
        walk_sound = self.base.walk_sound

        if self.is_on_ground or self.is_flying:
            if key_map['w'] or key_map['a'] or key_map['s'] or key_map['d']:
                self.is_walking = True
                if walk_sound.status() is not walk_sound.PLAYING:
                    walk_sound.play()
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
                self.is_walking = False
                if walk_sound.status() is walk_sound.PLAYING:
                    walk_sound.stop()
                self.velocity = Vec3(0, 0, 0)

            if key_map['space']:
                if self.is_on_ground:
                    self.base.jump_sound.play()
                self.is_on_ground = False
                self.is_flying = False
                self.velocity.setZ(Player.jump_speed)

    def update_position(self):
        self.update_velocity()
        dt = globalClock.getDt()
        self.position = self.position + self.velocity * dt

        floor_height = self.base.block.get_floor_height() + 1

        # # ジャンプ中の位置情報を保存
        # self.record_jump_positions_with_time(dt, floor_height)

        key_map = self.key_map
        if key_map['arrow_up']:
            self.is_on_ground = False
            self.is_flying = True
            self.position.setZ(self.position.getZ() + Player.jump_speed * dt)
        elif key_map['arrow_down']:
            self.position.setZ(self.position.getZ() - Player.jump_speed * dt)
            if self.position.z <= floor_height:
                self.position.z = floor_height
                self.is_on_ground = True
                self.is_flying = False

        if not self.is_flying:
            if not self.is_on_ground:
                if self.position.z <= floor_height:
                    self.position.z = floor_height
                    self.is_on_ground = True
                    self.base.landing_of_jump_sound.play()
                else:
                    self.velocity.setZ(self.velocity.getZ() - Player.gravity_force * dt)
            else:
                if floor_height < self.position.z:
                    self.is_on_ground = False
                    self.velocity.setZ(-Player.gravity_force * dt)

    def draw(self):
        self.base.player_node.setH(self.direction.x)
        self.base.player_head_node.setP(self.direction.y)
        # # ブロックと干渉したとき位置を修正
        self.change_position_when_interfering_with_block()
        self.base.player_node.setPos(self.position)

    def player_update(self, task):
        self.update_direction()
        self.update_position()
        self.draw()
        return task.cont

    def update_motion(self, task):
        if self.is_walking:
            self.walking_count += 1
            if self.walking_count % 2:
                self.base.player_right_hand_node.setP(70)
                self.base.player_left_hand_node.setP(110)
                self.base.player_right_leg_node.setP(20)
                self.base.player_left_leg_node.setP(-20)
            else:
                self.base.player_right_hand_node.setP(110)
                self.base.player_left_hand_node.setP(70)
                self.base.player_right_leg_node.setP(-20)
                self.base.player_left_leg_node.setP(20)
        else:
            self.base.player_right_hand_node.setP(90)
            self.base.player_left_hand_node.setP(90)
            self.base.player_right_leg_node.setP(0)
            self.base.player_left_leg_node.setP(0)
        return task.again

    def player_add_block(self):
        block_id = self.base.hotbar_blocks[self.base.selected_hotbar_num][0]
        if self.target_position and \
                not self.base.block.is_block_at(self.target_position):
            self.base.block.add_block(
                self.target_position.x,
                self.target_position.y,
                self.target_position.z,
                block_id
            )

    def player_remove_block(self):
        if self.target_position and \
                self.base.block.is_block_at(self.target_position):
            self.base.block.remove_block(
                self.target_position.x,
                self.target_position.y,
                self.target_position.z
            )

    def change_position_when_interfering_with_block(self):
        velocity_x, velocity_y, velocity_z = self.velocity
        x, y, z = self.position
        # X方向の干渉チェック
        if 0 < velocity_x:
            x_to_check = x + 0.5
            if self.base.block.is_block_at(Point3(x_to_check, y, z)) or \
                    self.base.block.is_block_at(Point3(x_to_check, y, z + 1)):
                x = floor(x_to_check) - 1
        elif velocity_x < 0:
            x_to_check = x - 0.5
            if self.base.block.is_block_at(Point3(x_to_check, y, z)) or \
                    self.base.block.is_block_at(Point3(x_to_check, y, z)):
                x = floor(x_to_check) + 2
        # Y方向の干渉チェック
        if 0 < velocity_y:
            y_to_check = y + 0.5
            if self.base.block.is_block_at(Point3(x, y_to_check, z)) or \
                    self.base.block.is_block_at(Point3(x, y_to_check, z + 1)):
                y = floor(y_to_check) - 1
        elif velocity_y < 0:
            y_to_check = y - 0.5
            if self.base.block.is_block_at(Point3(x, y_to_check, z)) or \
                    self.base.block.is_block_at(Point3(x, y_to_check, z + 1)):
                y = floor(y_to_check) + 2
        # Z方向の干渉チェック
        if 0 < velocity_z:
            z_to_check = z + 2
            if self.base.block.is_block_at(Point3(x, y, z_to_check)):
                z = floor(z_to_check) - 2
                self.velocity.setZ(0)
        self.position = Point3(x, y, z)

    # ジャンプ中の位置を記録する
    def record_jump_positions_with_time(self, dt, floor_height):
        if self.is_on_ground:
            self.passed_time_of_jump = 0
            self.jump_positions_with_time = [(0, *self.position)]
        else:
            self.passed_time_of_jump += dt
            self.jump_positions_with_time.append((self.passed_time_of_jump, *self.position))
            if self.position.z <= floor_height:
                if self.jump_positions_with_time:
                    print(self.jump_positions_with_time)
