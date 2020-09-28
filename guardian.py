#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from maze import Maze
from image import Image


class Guardian:

    def __init__(self):
        self.position = x_coordinate, y_coordinate = Maze.location(Maze.EXIT)
        self.image, self.rect = Image.load("Gardien.png")
        self.rect.x = x_coordinate * self.rect.width
        self.rect.y = y_coordinate * self.rect.height
