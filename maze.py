#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
from image import Image

class Maze:

    ZONES = {}
    MIN_WIDTH, MAX_WIDTH = 0, 14
    MIN_HEIGHT, MAX_HEIGHT = 0, 14
    WIDTH, HEIGHT = 15, 15

    STRUCTURE_WALL = "Wall"
    STRUCTURE_PATH = "Path"
    STRUCTURE_START = "MacGyver"
    STRUCTURE_EXIT = "Guardian"

    def __init__(self):
        # (0...19, 0...12)
        wall_position = 9, 11
        path_position = 0, 2
        crop_width, crop_height = 20, 20
        self.wall_image, self.wall_rect = Image.load_crop("floor-tiles-20x20.png",
            wall_position, crop_width, crop_height)
        self.path_image, self.path_rect = Image.load_crop("floor-tiles-20x20.png",
            path_position, crop_width, crop_height)

        self._init_zones()

    @classmethod
    def _init_zones(cls):
        structures = {
            cls.STRUCTURE_WALL: "#",
            cls.STRUCTURE_PATH: " ",
            cls.STRUCTURE_START: "?",
            cls.STRUCTURE_EXIT: "!"
        }
        counters = {
            cls.STRUCTURE_WALL: 0,
            cls.STRUCTURE_PATH: 0,
            cls.STRUCTURE_START: 0,
            cls.STRUCTURE_EXIT: 0
        }

        subdirectory = "config"
        configuration_file = "maze.txt"
        working_directory = os.path.dirname(__file__)
        configuration_file = os.path.join(working_directory, subdirectory, configuration_file)
        try:
            with open(configuration_file, 'r') as config_file:
                for line_number, line in enumerate(config_file):
                    for char_number, char in enumerate(line):
                        structure = "Unknown"
                        for structure_key in structures:
                            if char == structures[structure_key]:
                                structure = structure_key
                                break
                        if structure != "Unknown":
                            cls.ZONES[(char_number, line_number - 1)] = structure
                            counters[structure] += 1

        except FileNotFoundError:
            print("The configuration file was not found:", configuration_file)
            sys.exit()
        except PermissionError:
            print("You don't have the adequate rights to read the configuration file:",
            configuration_file)
            sys.exit()
        else:
            if (counters[cls.STRUCTURE_START] < 1 or
                counters[cls.STRUCTURE_EXIT] < 1 or
                counters[cls.STRUCTURE_PATH] < 3):
                try:
                    raise RuntimeError("The configuration file is corrupted:",
                        format(configuration_file))
                except RuntimeError:
                    print("The configuration file is corrupted:", format(configuration_file))
                    sys.exit()

    @classmethod
    def location(cls, structure):
        for coordinates in cls.ZONES:
            if cls.ZONES[coordinates] == structure:
                location = coordinates
                break
        return location

    @classmethod
    def free_paths(cls):
        return [coordinates for coordinates in cls.ZONES
            if cls.ZONES[coordinates] == cls.STRUCTURE_PATH]
