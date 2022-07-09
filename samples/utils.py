"""
Utilities
"""
from math import *
from time import time

from panda3d.core import *
from direct.particles.ParticleEffect import ParticleEffect
from direct.showbase.ShowBaseGlobal import globalClock


def turn_on_light(base):
    # point light
    plight = PointLight('plight')
    plight.setColor((0.2, 0.2, 0.2, 1))
    plnp = base.render.attachNewNode(plight)
    plnp.setPos(10, 20, 0)
    base.render.setLight(plnp)

    # # directional light
    # dlight = DirectionalLight('dlight')
    # dlight.setColor((0.8, 0.8, 0.5, 1))
    # dlnp = base.render.attachNewNode(dlight)
    # dlnp.setHpr(0, -60, 0)
    # base.render.setLight(dlnp)

    # ambient light
    alight = AmbientLight('alight')
    alight.setColor((1, 1, 1, 0.5))
    alnp = base.render.attachNewNode(alight)
    base.render.setLight(alnp)


def get_length(start: Vec3, end: Vec3):
    line_vec = end - start
    return line_vec.length()


def get_polar_angles(start: Vec3, end: Vec3):
    if get_length(start, end):
        line_vec = end - start
        x, y, z = line_vec[0], line_vec[1], line_vec[2]
        theta = degrees(acos(z / sqrt(x ** 2 + y ** 2 + z ** 2)))
        phi = degrees(atan2(y, x))
    else:
        theta, phi = 0, 0
    return theta, phi


def get_angles_between_two_lines(positions, points_list):
    angles = []
    for points in points_list:
        parent_vec = (Vec3(*positions[points[0][0]]) - Vec3(*positions[points[0][1]])).normalized()
        child_vec = (Vec3(*positions[points[1][0]]) - Vec3(*positions[points[1][1]])).normalized()
        angles.append(child_vec.angleDeg(parent_vec))
    return angles


def make_globe_model(base):
    base.left_globe_model = base.loader.loadModel('models/sphere12')
    base.left_globe_model.setColor(base.globe_colors[1])
    base.left_globe_model.setScale(20)
    base.left_globe_model.reparentTo(base.get(f'left_point_node9'))
    base.left_globe_model.hide()
    base.right_globe_model = base.loader.loadModel('models/sphere12')
    base.right_globe_model.setColor(base.globe_colors[0])
    base.right_globe_model.setScale(20)
    base.right_globe_model.reparentTo(base.get(f'right_point_node9'))
    base.right_globe_model.hide()


def draw_globe(base):
    if base.hand_positions:
        for hand_name in base.hand_names:
            hand_instance = base.get(hand_name)
            globe_model = base.get(f'{hand_name}_globe_model')
            if hand_instance['gesture_name'] == 'zero' or hand_instance['gesture_name'] == 'nice':
                base.set(f'{hand_name}_globe_start_time', time())
                if globe_model.isHidden():
                    globe_model.show()
            else:
                start_time = base.get(f'{hand_name}_globe_start_time')
                end_time = time()
                if start_time and end_time - start_time > base.allowable_passed_time:
                    if not globe_model.isHidden():
                        globe_model.hide()
    else:
        for hand_name in base.hand_names:
            globe_model = base.get(f'{hand_name}_globe_model')
            start_time = base.get(f'{hand_name}_globe_start_time')
            end_time = time()
            if start_time and end_time - start_time > base.allowable_passed_time:
                if not globe_model.isHidden():
                    globe_model.hide()


def grid(base, line_num=20, step=10, position=None, color=None):
    if position is None:
        position = (-line_num * step / 2, line_num * step / 2, -line_num * step / 2)
    if color is None:
        color = (1, 1, 1, 0.3)
    geom_format = GeomVertexFormat.getV3c4()
    geom_vertex_data = GeomVertexData('', geom_format, Geom.UHDynamic)
    vertex_writer = GeomVertexWriter(geom_vertex_data, 'vertex')
    color_writer = GeomVertexWriter(geom_vertex_data, 'color')
    index_data = []
    for i in range(line_num + 1):
        vertex_writer.addData3(Vec3(0, 0, i) * step)
        color_writer.addData4f(*color)
        vertex_writer.addData3(Vec3(line_num, 0, i) * step)
        color_writer.addData4f(*color)
        vertex_writer.addData3(Vec3(i, 0, 0) * step)
        color_writer.addData4f(*color)
        vertex_writer.addData3(Vec3(i, 0, line_num) * step)
        color_writer.addData4f(*color)
        index_data.append((i * 4, i * 4 + 1))
        index_data.append((i * 4 + 2, i * 4 + 3))

    geom_lines = GeomLines(Geom.UHDynamic)
    for index in index_data:
        geom_lines.addVertices(*index)
    geom = Geom(geom_vertex_data)
    geom.addPrimitive(geom_lines)

    base.grid_node = base.render.attachNewNode(PandaNode('grid_node'))
    base.grid_node.setPos(*position)
    translates = [
        (0, 0, 0, 0, 0, 0),
        (0, 0, line_num * step, 0, 90, 0),
        (0, 0, 0, 0, 90, 0),
        (0, 0, 0, -90, 0, 0),
        (line_num * step, 0, 0, -90, 0, 0),
        # (0, -line_num * step, 0, 0, 0, 0),
    ]

    for translate in translates:
        geom_node = GeomNode('')
        geom_node.addGeom(geom)
        node = base.grid_node.attachNewNode(geom_node)
        node.setPosHpr(*translate)
        node.setTransparency(TransparencyAttrib.MAlpha)


def load_particle(base, particle_name, parent):
    base.set(f'particle_{particle_name}', ParticleEffect())
    particle = base.get(f'particle_{particle_name}')
    particle.loadConfig(f'particles/{particle_name}.ptf')
    particle.start(parent)
    particle.softStop()


def vec3_to_tuple(vec: Vec3):
    # return vec.getX(), vec.getY(), vec.getZ()
    return vec[0], vec[1], vec[2]


def distance_from_point_to_line(point: Point3, point_on_line: Point3, direction_vector: Vec3):
    x0, y0, z0 = vec3_to_tuple(point)
    a, b, c = vec3_to_tuple(point_on_line)
    p, q, r = vec3_to_tuple(direction_vector)
    # 内積が0になる媒介変数tを求める
    t = -((a - x0) * p + (b - y0) * q + (c - z0) * r) / sqrt(p ** 2 + q ** 2 + r ** 2)
    # 最も近い線上の点の座標を求める
    x = a + p * t
    y = b + q * t
    z = c + r * t
    # 点と線の距離
    length = sqrt((x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2)
    return length


def set_camera(base):
    r, theta, phi = base.camera_radius, base.camera_theta, base.camera_phi
    x = r * sin(radians(theta)) * cos(radians(phi))
    y = r * sin(radians(theta)) * sin(radians(phi))
    z = r * cos(radians(theta))
    base.camera_position = Vec3(x, y, z)
    base.camera.setPos(base.camera_position)
    base.camera.lookAt(0, 0, 0)


def rotate_camera(base, task):
    dt = globalClock.getDt()
    base.camera_phi += dt * base.camera_rotational_speed
    set_camera(base)
    return task.cont


def control_camera_angle(base, task):
    key_map = base.key_map
    if key_map['r']:
        base.camera_theta = 90
        base.camera_phi = -90
    elif key_map['arrow_up']:
        base.camera_theta += 1
    elif key_map['arrow_down']:
        base.camera_theta -= 1
    elif key_map['arrow_right']:
        base.camera_phi += 1
    elif key_map['arrow_left']:
        base.camera_phi -= 1
    set_camera(base)
    return task.cont


def count_up_with_gtts(lang, num):
    sound = base.loader.loadMusic(f'sound/{lang}/{num % 100}.mp3')
    sound.setLoop(False)
    sound.setVolume(5)
    sound.play()


if __name__ == '__main__':
    # vec1 = Vec3(1, 0, 0)
    # vec2 = Vec3(0, 3, 0)
    # point1 = Point3(1, 0, 0)
    # point2 = Point3(2, 0, 0)
    # print(vec1.angleDeg(vec2))
    # print(vec1.angleDeg(vec2.normalized()))
    # print(vec2.normalized().angleDeg(vec1))
    # print(vec3_to_tuple(vec1))
    # print(distance_from_point_to_line(point1, point2, vec1))
    # print(distance_from_point_to_line(point1, point2, vec2))
    from direct.showbase.ShowBase import ShowBase
    from panda3d.core import *

    showbase = ShowBase()
    grid(showbase)
    showbase.run()
