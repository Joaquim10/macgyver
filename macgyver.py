#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from maze import Maze
from items import Items
from image import Image

class MacGyver:

    def __init__(self):
        self.position = Maze.location(Maze.STRUCTURE_START)
        self.items_in_backpack = 0
        self.image, self.rect = Image.load("MacGyver.png")
        self.move(self.position)

    def move(self, position):
        self.position = position
        x_coordinate, y_coordinate = self.position
        self.rect.topleft = x_coordinate * self.rect.w, y_coordinate * self.rect.h

    def pick_up(self, item):
        Items.BACKPACK.append(item)
        self.items_in_backpack += 1

    def craft(self, item):
        for material in Items.BACKPACK:
            Items.USED.append(material)
        Items.BACKPACK.clear()
        self.items_in_backpack = 0
        self.pick_up(item)
