"""src/camera.py"""
from math import *
from panda3d.core import *


class Camera:
    far_length = 50
    base_camera_back = 5
    base_camera_height = 3
    base_camera_forward = 6
    base_cam_fov = 90
    player_cam_height = 1.5
    player_cam_fov = 100
    player_head_height = 0.8
    mirror_cam_radius = 5
    mirror_cam_film_size = (8, 6)

    def __init__(self, base):
        self.base = base

        # マウス操作を禁止
        base.disableMouse()
        # # カメラの設定
        # base.camera.setPos(10, -25, 15)
        # # base.camera.setPos(3, 6, 3)
        # base.camera.lookAt(0, 0, 0)

        # base cam
        base.cam.reparentTo(base.player_head_node)
        base.camLens.setFov(Camera.base_cam_fov)
        # base.camLens.setFar(Camera.far_length)
        base.cam.setPos(
            Vec3(0, -Camera.base_camera_back, Camera.base_camera_height)
        )
        base.cam.lookAt(
            Vec3(0, Camera.base_camera_forward, 0)
        )

        # player cam
        player_cam_lens = PerspectiveLens()
        player_cam_lens.setFov(Camera.player_cam_fov)
        player_cam_lens.setNear(0.1)
        player_cam_lens.setFar(Camera.far_length)
        self.player_cam = base.makeCamera(base.win)
        self.player_cam.node().setLens(player_cam_lens)
        self.player_cam.reparentTo(base.player_head_node)
        self.player_cam.setPos(
            Vec3(0, Camera.player_head_height / 2, 0)
        )

        # mirror cam
        mirror_cam_lens = OrthographicLens()
        mirror_cam_lens.setFilmSize(*Camera.mirror_cam_film_size)
        mirror_cam_lens.setFar(Camera.far_length)
        mirror_cam_lens.setNear(-100)
        self.mirror_cam = base.makeCamera(base.win)
        self.mirror_cam.node().setLens(mirror_cam_lens)
        self.mirror_cam.reparentTo(base.player_head_node)
        self.mirror_cam.setPos(
            Vec3(0, Camera.mirror_cam_radius, 0)
        )
        self.mirror_cam.setH(180)

        # カメラ設定
        # base.cameras = [base.cam, self.player_cam]
        base.cameras = [base.cam, self.player_cam, self.mirror_cam]
        base.activeCam = 0
        base.cameras[1].node().getDisplayRegion(0).setActive(0)
        base.cameras[2].node().getDisplayRegion(0).setActive(0)

        # カメラを切り替え
        base.accept('t', self.toggle_cam)

    def toggle_cam(self):
        self.base.cameras[self.base.activeCam].node().getDisplayRegion(0).setActive(0)
        self.base.activeCam = (self.base.activeCam + 1) % len(self.base.cameras)
        self.base.cameras[self.base.activeCam].node().getDisplayRegion(0).setActive(1)
        # if self.base.activeCam == 1:
        #     self.base.player_node.hide()
        # else:
        #     self.base.player_node.show()

