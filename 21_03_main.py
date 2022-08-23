"""21_03_main.py"""
from src import MC


class Game(MC):
    def __init__(self):
        # MCを継承する
        MC.__init__(self, ground_size=256, cloud_range=256)


game = Game()
game.run()
