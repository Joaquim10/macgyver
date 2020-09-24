#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import random
from item import Item
from maze import Maze

class Items:

    free_paths = []
    LOOT = []
    BACKPACK = []
    USED = []

    def __init__(self):
        self.syringe = Item("syringe", (-1, -1))
        self.free_paths = Maze.free_paths()
        for item_name in ["needle", "tube", "ether"]:
        # Drop items on random free paths
            location = random.choice(self.free_paths)
            self.LOOT.append(Item(item_name, location))
            self.free_paths.remove(location)
