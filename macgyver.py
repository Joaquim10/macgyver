#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from maze import Maze
from image import Image

class MacGyver:

    def __init__(self):
        self.position = Maze.location(Maze.STRUCTURE_START)
        self.items_in_backpack = 0
        self.backpack = []
        self.image, self.rect = Image.load("MacGyver.png")
        self.move(self.position)

    def move(self, position):
        self.position = position
        x_coordinate, y_coordinate = self.position
        self.rect.topleft = x_coordinate * Image.WIDTH, y_coordinate * Image.HEIGHT

    def pick_up(self, item):
        self.backpack.append(item)
        self.items_in_backpack += 1

    def craft(self, item):
        self.backpack.clear()
        self.items_in_backpack = 0
        self.pick_up(item)
