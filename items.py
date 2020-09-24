#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import random
from item import Item
from maze import Maze

class Items:

    free_paths = []
    loot = []
    backpack = []

    def __init__(self):
        self.items_in_backpack = 0
        self.syringe = Item("syringe", "seringue.png", (0,0), quality="crafted")
        self.drop()

    def drop(self):
        """Drop items on random free paths"""
        items = {
            "needle": "aiguille.png",
            "tube": "tube_plastique.png",
            "ether": "ether.png"
        }
        self.free_paths = Maze.free_paths()
        for name in items:
            location = random.choice(self.free_paths)
            self.loot.append(Item(name, items[name], location, "material"))
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
