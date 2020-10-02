#!/usr/bin/python3
# -*- coding: UTF-8 -*-


from image import Image


class Item:

    def __init__(self, **kwargs):
        """def __init__(self, name, description, image_file, image_size,
                        position=(-1, -1), quality="material"):"""
        self.name = kwargs["name"]
        self.description = kwargs["description"]
        if "position" in kwargs:
            self.position = kwargs["position"]
        else:
            self.position = (-1, -1)
        self.image = Image.load(kwargs["image_file"], kwargs["image_size"])
        if "quality" in kwargs:
            self.quality = kwargs["quality"]
        else:
            self.quality = "material"
