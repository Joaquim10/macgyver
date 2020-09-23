#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from maze import Maze
from image import Image

class Guardian:

    def __init__(self):
        self.position = Maze.location(Maze.STRUCTURE_EXIT)
        self.image, self.rect = Image.load("Gardien.png")
        x_coordinate, y_coordinate = self.position
        self.rect.topleft = x_coordinate * Image.WIDTH, y_coordinate * Image.HEIGHT
