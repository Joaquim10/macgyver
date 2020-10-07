#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

item: item contains the class Item.

Classes:
    Item: The Item object represents an item.
"""

from app.pgimage import PgImage


class Item:
    """

    The Item object represents an item.

    Args:
        **kwargs: The keyword arguments are used for initializing an item.
            "name" (str): Name of the item.
            "description" (str): Description of the item.
            "position" (tuples, optional): Coordinates of the item in the
                labyrinth. Default is (-1, -1).
            "image_file" (str): File name of the image for the item.
            "image_size" (tuples): Width and height for the image of the item.
            "quality" (str, optional): Quality of the item. Default is
                "material".

    Attributes:
        name (str): The name of the item.
        description (str): A description of the item.
        position (tuples): Coordinates of the item in the labyrinth.
        image (pygame.Surface): Image of the item.
        quality (str): Quality of the item.
    """
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.description = kwargs["description"]
        if "position" in kwargs:
            self.position = kwargs["position"]
        else:
            self.position = (-1, -1)
        self.image = PgImage.load(kwargs["image_file"], kwargs["image_size"])
        if "quality" in kwargs:
            self.quality = kwargs["quality"]
        else:
            self.quality = "material"