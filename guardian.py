#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from const import Const
from maze import Maze
from image import Image


class Guardian:

    def __init__(self, image_size):
        self.position = Maze.location(Const.MAZE_EXIT)
        self.image = Image.load("Gardien.png", image_size)
