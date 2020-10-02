#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys

from const import Const
from image import Image


class Maze:

    zones = {}

    def __init__(self, image_size):
        self.wall_image = Image.load_crop("floor-tiles-20x20.png",
                                          Const.CROP_WALL_POSITION,
                                          Const.CROP_SIZE,
                                          image_size)
        self.path_image = Image.load_crop("floor-tiles-20x20.png",
                                          Const.CROP_PATH_POSITION,
                                          Const.CROP_SIZE,
                                          image_size)
        self._init_zones()

    @classmethod
    def _init_zones(cls):
        structures = {
            Const.MAZE_WALL: "#",
            Const.MAZE_PATH: " ",
            Const.MAZE_START: "?",
            Const.MAZE_EXIT: "!"
        }
        counters = {
            Const.MAZE_WALL: 0,
            Const.MAZE_PATH: 0,
            Const.MAZE_START: 0,
            Const.MAZE_EXIT: 0
        }
        working_directory = os.path.dirname(__file__)
        configuration_file = os.path.join(working_directory, Const.CONFIG_DIR,
                                          Const.CONFIG_FILE)
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
                            cls.zones[(char_number, line_number-1)] = structure
                            counters[structure] += 1
        except FileNotFoundError:
            print("The configuration file was not found:", configuration_file)
            sys.exit()
        except PermissionError:
            print("You don't have the adequate rights to read "
                  "the configuration file:", configuration_file)
            sys.exit()
        else:
            if (counters[Const.MAZE_START] < 1 or
                    counters[Const.MAZE_EXIT] < 1 or
                    counters[Const.MAZE_PATH] < 3):
                try:
                    raise RuntimeError("The configuration file is corrupted:",
                                       configuration_file)
                except RuntimeError:
                    print("The configuration file is corrupted:",
                          configuration_file)
                    sys.exit()

    @classmethod
    def location(cls, structure):
        for coordinates in cls.zones:
            if cls.zones[coordinates] == structure:
                location = coordinates
                break
        return location

    @classmethod
    def free_paths(cls):
        return [coordinates for coordinates in cls.zones
                if cls.zones[coordinates] == Const.MAZE_PATH]

    @staticmethod
    def collision_detected(location):
        x_coordinate, y_coordinate = location
        return Maze.zones[location] == Const.MAZE_WALL or \
            x_coordinate < Const.MAZE_MIN_WIDTH or \
            x_coordinate > Const.MAZE_WIDTH - 1 or \
            y_coordinate < Const.MAZE_MIN_HEIGHT or \
            y_coordinate > Const.MAZE_HEIGHT - 1
