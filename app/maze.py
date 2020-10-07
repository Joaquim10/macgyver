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

import sys

import config.const as const
import config.settings as settings
from app.tools import Tools
from app.pgimage import PgImage


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
        self.wall_image = PgImage.load_crop(const.TEXTURE_ATLAS,
                                            const.CROP_WALL_POSITION,
                                            const.CROP_SIZE,
                                            image_size)
        self.path_image = PgImage.load_crop(const.TEXTURE_ATLAS,
                                            const.CROP_PATH_POSITION,
                                            const.CROP_SIZE,
                                            image_size)
        self._init_zones()

    @classmethod
    def _init_zones(cls):
        '''

        Initializes the zones of the labyrinth.

        Opens the configuration file, initializes the zones of the labyrinth
        and checks for errors. If an error is found, the program exits.
        '''
        structures = {
            const.MAZE_WALL: "#",
            const.MAZE_PATH: " ",
            const.MAZE_START: "?",
            const.MAZE_EXIT: "!"
        }
        counters = {
            const.MAZE_WALL: 0,
            const.MAZE_PATH: 0,
            const.MAZE_START: 0,
            const.MAZE_EXIT: 0
        }
        maze_file = Tools.full_name(const.MAZES_DIR, settings.MAZE_FILE)
        try:
            with open(maze_file, 'r') as tile_set_file:
                for line_number, line in enumerate(tile_set_file):
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
            print("The configuration file was not found:", maze_file)
            sys.exit()
        except PermissionError:
            print("You don't have the adequate rights to read the maze file:",
                  maze_file)
            sys.exit()
        else:
            if (len(cls.zones) != const.MAZE_WIDTH * const.MAZE_HEIGHT or
                    counters[const.MAZE_START] < 1 or
                    counters[const.MAZE_EXIT] < 1 or
                    counters[const.MAZE_PATH] < 3):
                try:
                    raise RuntimeError("The configuration file is corrupted:",
                                       maze_file)
                except RuntimeError:
                    print("The configuration file is corrupted:", maze_file)
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
                if cls.zones[coordinates] == const.MAZE_PATH]

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
        return Maze.zones[location] == const.MAZE_WALL or \
            x_coordinate < const.MAZE_MIN_WIDTH or \
            x_coordinate > const.MAZE_WIDTH - 1 or \
            y_coordinate < const.MAZE_MIN_HEIGHT or \
            y_coordinate > const.MAZE_HEIGHT - 1
