#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import random

from item import Item
from maze import Maze


class Items:

    free_paths = []
    materials = []
    backpack = []

    def __init__(self, image_size):
        crafts = {
            "syringe": {
                "name": "syringe",
                "description": "an epidermic syringe",
                "image_file": "seringue.png",
                "quality": "craft"
            }
        }
        self.items_in_backpack = 0
        crafts["syringe"].update({"image_size": image_size})
        self.syringe = Item(**crafts["syringe"])
        self.drop(image_size)

    def drop(self, image_size):
        """Drop items on random free paths"""
        materials = {
            "needle": {
                "name": "needle",
                "description": "a needle",
                "image_file": "aiguille.png",
                "quality": "material"
            },
            "tube": {
                "name": "tube",
                "description": "a little plastic tube",
                "image_file": "tube_plastique.png",
                "quality": "material"
            },
            "ether": {
                "name": "ether",
                "description": "some ether",
                "image_file": "ether.png",
                "quality": "material"
            }
        }
        self.free_paths = Maze.free_paths()
        for material in materials:
            location = random.choice(self.free_paths)
            kwargs = {"position": location, "image_size": image_size}
            materials[material].update(kwargs)
            item = Item(**materials[material])
            self.materials.append(item)
            self.free_paths.remove(location)

    def pick_up(self, item):
        self.backpack.append(item)
        self.items_in_backpack += 1
        if item in self.materials:
            self.materials.remove(item)
        self.free_paths.append(item.position)

    def craft(self):
        for item in self.backpack:
            if item.quality == "material":
                item.quality = "destroyed"
        self.items_in_backpack = 0
        self.pick_up(self.syringe)
