#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

items: items contains the class Items.

Classes:
    Items: The Items object handles all the items.

Methods:
    pick_up(item):
        Adds an item to MacGyver's backpack.
    craft():
        Add the syringe to MacGyver's backpack and destroy other items.
"""

import random

from item import Item
from maze import Maze


class Items:
    """

    The Items object handles with items.

    free_paths = []
    materials = []
    backpack = []

    Args:
        image_size(couple of tuples):
            Width and height for the images of the items.

    Class attributes:
        free_paths (list): Coordinates of the free paths.
        materials (list): Items dropped across the maze.
        backpack (list): Items in MacGyver's backpack.

    Attributes:
        items_in_backpack (int): Counter for items in MacGyver's backpack.
        syringe (Item): syringue item.
    """
    free_paths = []
    materials = []
    backpack = []

    def __init__(self, image_size):
        self.items_in_backpack = 0
        self.syringe = self._syringe(image_size)
        self._drop(image_size)

    @staticmethod
    def _syringe(image_size):
        """Initialize and return the syringe item."""
        crafts = {
            "syringe": {
                "name": "syringe",
                "description": "an epidermic syringe",
                "image_file": "seringue.png",
                "quality": "craft"
            }
        }
        crafts["syringe"].update({"image_size": image_size})
        return Item(**crafts["syringe"])

    def _drop(self, image_size):
        """

        Drop the items on random free paths.

        This method initializes the items and the free paths list and updates
        the materials and free paths list.
        """
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
        '''

        Adds an item to MacGyver's backpack.

        This method update the items in MacGyver's backpack count and the
        backpack, materials and free paths lists.

            Args:
                item (Item): The item got by MacGyver.
        '''
        self.backpack.append(item)
        self.items_in_backpack += 1
        if item in self.materials:
            self.materials.remove(item)
        self.free_paths.append(item.position)

    def craft(self):
        '''

        Add the syringe to MacGyver's backpack and destroy other items.

        This method updating the qualities
        of others items in MacGyver's backpack resetting the items in
        MacGyver's backpack counter to 0.
        '''
        for item in self.backpack:
            if item.quality == "material":
                item.quality = "destroyed"
        self.items_in_backpack = 0
        self.pick_up(self.syringe)
