#!/usr/bin/python3
# -*- coding: UTF-8 -*-


from image import Image


class Item:

    def __init__(self, name, image, description="", position=(-1, -1)):
        self.name = name
        self.description = description
        self.position = x_coordinate, y_coordinate = position
        self.quality = "material"
        self.image, self.rect = Image.load(image)
        self.rect.x = x_coordinate * self.rect.width
        self.rect.y = y_coordinate * self.rect.height
