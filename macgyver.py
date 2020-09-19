#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class Maze:

    ZONES = {}
    MIN_WIDTH, MAX_WIDTH = 0, 14
    MIN_HEIGHT, MAX_HEIGHT = 0, 14

    STRUCTURE_WALL = "Wall"
    STRUCTURE_PATH = "Path"
    STRUCTURE_START = "MacGyver"
    STRUCTURE_EXIT = "Guardian"
