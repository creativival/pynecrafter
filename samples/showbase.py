"""Panda3D ShowBase"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *


class App(ShowBase):
    pass


if __name__ == '__main__':
    app = App()
    app.run()
