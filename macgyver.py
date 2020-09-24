#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from maze import Maze
from image import Image

class MacGyver:

    def __init__(self):
        self.position = Maze.location(Maze.STRUCTURE_START)
        self.image, self.rect = Image.load("MacGyver.png")
        self.move(self.position)

    def move(self, position):
        self.position = position
        x_coordinate, y_coordinate = self.position
        self.rect.topleft = x_coordinate * self.rect.w, y_coordinate * self.rect.h
