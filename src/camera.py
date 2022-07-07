"""src/camera.py"""
from math import *
from panda3d.core import *


class Camera:
    # base_camera_back = 6
    # base_camera_height = 6
    # base_camera_forward = 6
    # base_cam_fov = 90
    # player_cam_height = 1.5
    # player_cam_fov = 100
    # player_head_height = 0.5
    # mirror_cam_radius = 5
    # mirror_cam_film_size = (4, 3)
    # perspective_lens = PerspectiveLens()
    # perspective_lens.setFov(player_cam_fov)

    def __init__(self, base):
        self.base = base

        # マウス操作を禁止
        base.disableMouse()
        # カメラの設定
        base.camera.setPos(10, -25, 15)
        # base.camera.setPos(3, 6, 3)
        base.camera.lookAt(0, 0, 0)

    #     # base cam
    #     base.cam.reparentTo(base.player_node)
    #     base.camLens.setFov(Camera.base_cam_fov)
    #     base.cam.setPos(
    #         Vec3(0, -Camera.base_camera_back, Camera.base_camera_height)
    #     )
    #     base.cam.lookAt(
    #         Vec3(0, Camera.base_camera_forward, 0)
    #     )
    #     # player cam
    #     self.player_cam = base.makeCamera(base.win)
    #     self.player_cam.node().setLens(Camera.perspective_lens)
    #     self.player_cam.reparentTo(base.player_head_node)
    #     self.player_cam.setPos(
    #         Vec3(0, -Camera.player_head_height / 2, Camera.player_head_height / 2)
    #     )
    #     self.player_cam.setH(180)
    #     # mirror cam
    #     self.mirror_cam = base.makeCamera(base.win)
    #     self.mirror_cam.node().setLens(Camera.perspective_lens)
    #     self.mirror_cam.reparentTo(base.player_head_node)
    #     self.mirror_cam.setPos(
    #         Vec3(0, -Camera.mirror_cam_radius, 0)
    #     )
    #     # camera change settings
    #     base.cameras = [base.cam, self.player_cam, self.mirror_cam]
    #     base.cameras[1].node().getDisplayRegion(0).setActive(0)
    #     base.cameras[2].node().getDisplayRegion(0).setActive(0)
    #     base.activeCam = 0
    #
    #     # カメラを切り替え
    #     base.accept('t', self.toggle_cam)
    #
    # def toggle_cam(self):
    #     self.base.cameras[self.base.activeCam].node().getDisplayRegion(0).setActive(0)
    #     self.base.activeCam = (self.base.activeCam + 1) % len(self.base.cameras)
    #     self.base.cameras[self.base.activeCam].node().getDisplayRegion(0).setActive(1)

