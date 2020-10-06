#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

maze: maze contains the class Maze.

Classes:
    Maze: The Maze object represents the labyrinth.

Methods:
    location(structure):
        Returns the coordinates of the first specified structure found.
    free_paths():
        Returns the list of coordinates of the paths of the labyrinth.
    collision_detected(location):
        Checks for collision detection.
"""

import os
import sys

from const import Const
from pgimage import PgImage


class Maze:
    """

    The Maze object represents the labyrinth.

    Class attributes:
        zones (dict [tuples, str]): Dictionnary of the zones of the labyrinth.
        The keys are the coordinates of the zone and the values are the types
        of structures of the zones.

    Attributes:
        wall_image (pygame.Surface): Image of a wall tile.
        path_image (pygame.Surface): Image of a path.
    """
    zones = {}

    def __init__(self, image_size):
        self.wall_image = PgImage.load_crop("floor-tiles-20x20.png",
                                            Const.CROP_WALL_POSITION,
                                            Const.CROP_SIZE,
                                            image_size)
        self.path_image = PgImage.load_crop("floor-tiles-20x20.png",
                                            Const.CROP_PATH_POSITION,
                                            Const.CROP_SIZE,
                                            image_size)
        self._init_zones()

    @classmethod
    def _init_zones(cls):
        """

        Initializes the zones of the labyrinth.

        Opens the configuration file, initializes the zones of the labyrinth
        and checks for errors. If an error is found, the program exits.
        """
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
            if (len(cls.zones) != Const.MAZE_WIDTH * Const.MAZE_HEIGHT or
                    counters[Const.MAZE_START] < 1 or
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
        '''

        Returns the coordinates of the first specified structure found.

            Args:
                structure (str): The structure which coordinates are needed.

            Returns:
                location (tuples):
                The coordinates of the first specified structure found.
        '''
        for coordinates in cls.zones:
            if cls.zones[coordinates] == structure:
                location = coordinates
                break
        return location

    @classmethod
    def free_paths(cls):
        '''Returns the list of coordinates of the paths of the labyrinth.'''
        return [coordinates for coordinates in cls.zones
                if cls.zones[coordinates] == Const.MAZE_PATH]

    @staticmethod
    def collision_detected(location):
        '''

        Checks for collision detection.

            Args:
                location (tuples): The coordinates of a location in the
                labyrinth.

            Returns:
                collision_detected (bool)
                Retuns True if the specified location is a wall or if the
                coordinates are out of the labyrinth.
                Returns False for any other case.
        '''
        x_coordinate, y_coordinate = location
        return Maze.zones[location] == Const.MAZE_WALL or \
            x_coordinate < Const.MAZE_MIN_WIDTH or \
            x_coordinate > Const.MAZE_WIDTH - 1 or \
            y_coordinate < Const.MAZE_MIN_HEIGHT or \
            y_coordinate > Const.MAZE_HEIGHT - 1
