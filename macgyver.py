#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from maze import Maze
from image import Image


class MacGyver:

    def __init__(self):
        self.position = Maze.location(Maze.START)
        self.image, self.rect = Image.load("MacGyver.png")
        self.move(self.position)

    def move(self, position):
        self.position = x_coordinate, y_coordinate = position
        self.rect.x = x_coordinate * self.rect.width
        self.rect.y = y_coordinate * self.rect.height
