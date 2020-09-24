#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Item:

    def __init__(self, name, position=(-1, -1), quality="material"):
        self.name = name
        self.position = position
        self.quality = quality
