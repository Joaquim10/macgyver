#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

item: item contains the class Item.

Classes:
    Item: The Item object represents an item.
"""


class Item:
    """

    The Item object represents an item.

    Args:
        kwargs: The keyword arguments are used for initializing an item.
            ["name", (str)]: Name of the item.
            ["description", (str)]: Description of the item.
            ["image", (pygame.Surface)]: image for the item.
            ["position", (tuples, optional)]: Coordinates of the item in the
                labyrinth. Default is (-1, -1).
            ["quality", (str, optional)]: Quality of the item. Default is
                "material".

    Attributes:
        name (str): The name of the item.
        description (str): A description of the item.
        position (tuples): Coordinates of the item in the labyrinth.
        image (pygame.Surface): Image of the item.
        quality (str): Quality of the item.
    """
    def __init__(self, kwargs):
        self.name = kwargs["name"]
        self.description = kwargs["description"]
        self.image = kwargs["image"]
        if "position" in kwargs:
            self.position = kwargs["position"]
        else:
            self.position = (-1, -1)
        if "quality" in kwargs:
            self.quality = kwargs["quality"]
        else:
            self.quality = "material"
