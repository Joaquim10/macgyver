#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import random
from item import Item
from maze import Maze

class Items:

    free_paths = []
    loot = []
    backpack = []
    syringe = Item("syringe", quality="crafted")

    def __init__(self):
        self.items_in_backpack = 0
        # Drop items on random free paths
        self.free_paths = Maze.free_paths()
        for item_name in ["needle", "tube", "ether"]:
            location = random.choice(self.free_paths)
            self.loot.append(Item(item_name, location))
            self.free_paths.remove(location)

    def pick_up(self, item):
        self.backpack.append(item)
        self.items_in_backpack += 1
        if item in self.loot:
            self.loot.remove(item)
        self.free_paths.append(item.position)

    def craft(self):
        for material in self.backpack:
            material.quality = "destroyed"
        self.items_in_backpack = 0
        self.pick_up(self.syringe)
