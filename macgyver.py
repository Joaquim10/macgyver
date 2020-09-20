#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class MacGyver:

    def __init__(self, position):
        self.position = position
        self.items_in_backpack = 0

    def move(self, position):
        self.position = position

    def pick_up_item(self):
        self.items_in_backpack += 1

    def craft_item(self):
        return self.items_in_backpack >= 3
