#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class MacGyver:

    def __init__(self, position):
        self.position = position
        self.items_in_backpack = 0
        self.backpack = []

    def move(self, position):
        self.position = position

    def pick_up(self, item):
        self.backpack.append(item)
        self.items_in_backpack += 1

    def craft(self, item):
        self.backpack.clear()
        self.items_in_backpack = 0
        self.pick_up(item)
