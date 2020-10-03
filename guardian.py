#!./env/bin/python python3.7
# -*- coding: UTF-8 -*-

from const import Const
from maze import Maze
from pgimage import PgImage


class Guardian:

    def __init__(self, image_size):
        self.position = Maze.location(Const.MAZE_EXIT)
        self.image = PgImage.load("Gardien.png", image_size)
