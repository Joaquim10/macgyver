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

import config.const as const
from app.item import Item
from app.pgimage import PgImage


class Items:
    """

    The Items object handles with items.

    Args:
        image_size(tuples): Width and height for the images of the items.

    Attributes:
        materials (list [items.Items]): Items dropped across the maze.
        backpack (list [items.Items]): Items in MacGyver's backpack.
        items_in_backpack (int): Counter for items in MacGyver's backpack.
        free_paths (list [tuples]): Coordinates of the free paths.
        syringe (item.Item): syringue item.
    """
    def __init__(self, free_paths, image_size):
        self.materials = []
        self.backpack = []
        self.items_in_backpack = 0
        self.free_paths = free_paths
        self.syringe = self._syringe(image_size)
        self._drop(image_size)

    @staticmethod
    def _syringe(image_size):
        '''Initialize and return the syringe item.'''
        crafts = const.CRAFTS.copy()
        image = PgImage.load(crafts["syringe"]["image_file"], image_size)
        crafts["syringe"].pop("image_file")
        crafts["syringe"].update({"image": image})
        return Item(crafts["syringe"])

    def _drop(self, image_size):
        '''

        Drop the items on random free paths.

        This method initializes the items and the free paths list and updates
        the materials and free paths list.
        '''
        materials = const.MATERIALS.copy()
        for material in materials:
            location = random.choice(self.free_paths)
            image = PgImage.load(materials[material]["image_file"], image_size)
            materials[material].pop("image_file")
            kwargs = {"position": location, "image": image}
            materials[material].update(kwargs)
            item = Item(materials[material])
            self.materials.append(item)
            self.free_paths.remove(location)

    def pick_up(self, item):
        '''

        Adds an item to MacGyver's backpack.

        This method update the items in MacGyver's backpack count and the
        backpack, materials and free paths lists.

            Args:
                item (item.Item): The item got by MacGyver.
        '''
        self.backpack.append(item)
        self.items_in_backpack += 1
        if item in self.materials:
            self.materials.remove(item)
        self.free_paths.append(item.position)

    def craft(self):
        '''

        Adds the syringe to MacGyver's backpack and destroy other items.

        This method adds the syringe to MacGyver's backpack updating the
        qualities of others items in MacGyver's backpack and resetting the
        items in MacGyver's backpack counter to 0.
        '''
        for item in self.backpack:
            if item.quality == "material":
                item.quality = "destroyed"
                item.image = PgImage.redden(item.image)
        self.items_in_backpack = 0
        self.pick_up(self.syringe)
