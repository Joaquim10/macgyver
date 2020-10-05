#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

item: item contains the class Item.

Classes:
    Item: The Item object represents an item.
"""


from pgimage import PgImage


class Item:
    """

    The Item object represents an item.

    Args:
        **kwargs: The keyword arguments are used for initializing an item.
            **"name" (string): Name of the item.
            **"description" (string): Description of the item.
            **"position" (tuples, optional): Coordinates of the item in the
                labyrinth. Default is (-1, -1)
            **"image_file" (string): File name of the image for the item.
            **"image_size"(tuples): Width and height for the image of the item.
            **"quality" (string, optional): Quality of the item.
                Default is "material".

    Attributes:
        name (string): The name of the item.
        description (string): A description of the item.
        position (tuples): Coordinates of the item in the labyrinth.
        image (surface): Image of the item.
        quality (string): Quality of the item.
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
