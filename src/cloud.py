"""src/cloud.py"""
from panda3d.core import *
from . import make_perlin_noise
from direct.showbase.ShowBaseGlobal import globalClock


class Cloud:
    CLOUD_WAVELENGTH = 16
    CLOUD_MIN_RATE = 0.8
    CLOUD_ALTITUDE = 20
    CLOUD_HEIGHT = 2
    CLOUD_SPEED = 3
    # CLOUD_SPEED = 0  # TODO

    def __init__(self, cloud_range):
        self.cloud_node_position = Point3(0, 0, Cloud.CLOUD_ALTITUDE)
        self.cloud_models = []
        for i in range(50):
            color = i * 0.02
            cube = self.loader.loadModel('models/misc/rgbCube')
            cube.setColor(color, color, color)
            cube.setScale(1.0, 1.0, Cloud.CLOUD_HEIGHT)
            self.cloud_models.append(cube)

        perlin_noise = make_perlin_noise(wavelength=Cloud.CLOUD_WAVELENGTH, size=cloud_range)

        # 雲ブロックを置く
        self.cloud_node = self.render.attachNewNode(PandaNode('cloud_node'))
        for i in range(cloud_range):
            for j in range(cloud_range):
                noise = perlin_noise[j][i]
                if noise > Cloud.CLOUD_MIN_RATE:
                    num = int(noise / 0.02)
                    cloud_placeholder = self.cloud_node.attachNewNode(PandaNode('cloud_placeholder'))
                    cloud_placeholder.setPos(i - cloud_range / 2, j - cloud_range / 2, 0)
                    self.cloud_models[num].instanceTo(cloud_placeholder)


        self.taskMgr.add(self.cloud_update, 'cloud_update')

    def cloud_update(self, task):
        dt = globalClock.getDt()
        self.cloud_node_position.setX(self.cloud_node_position.x + Cloud.CLOUD_SPEED * dt)
        self.cloud_node.setPos(self.cloud_node_position)
        return task.cont
