#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from const import Const
from maze import Maze
from image import Image


class MacGyver():

    def __init__(self, image_size):
        self.position = Maze.location(Const.MAZE_START)
        self.image = Image.load("MacGyver.png", image_size)

    def move(self, position):
        self.position = position
