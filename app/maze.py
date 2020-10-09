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
        Returns the list of coordinates of the paths in the labyrinth.
    collision_detected(location):
        Checks for collision detection.
"""

import sys

import config.const as const
import config.settings as settings
from app.tools import Tools


class Maze:
    """

    The Maze object represents the labyrinth.

    Args:
        wall_image (pygame.Surface): Image for a wall tile.
        path_image (pygame.Surface): Image for a path tile.

    Attributes:
        zones (dict [tuples, str]): Dictionnary of the zones in the labyrinth.
            The keys are the coordinates of the zone and the values are the
            types of structures of the zones.
        wall_image (pygame.Surface): Image of a wall tile.
        path_image (pygame.Surface): Image of a path tile.
    """
    def __init__(self, wall_image, path_image):
        self.zones = {}
        self.wall_image = wall_image
        self.path_image = path_image
        self._init_zones()

    def _init_zones(self):
        '''

        Initializes the zones of the labyrinth.

        Opens the configuration file, initializes the zones of the labyrinth
        and checks for errors. If an error is found, the program exits.
        '''
        counters = {
            const.MAZE_WALL: 0,
            const.MAZE_PATH: 0,
            const.MAZE_START: 0,
            const.MAZE_EXIT: 0
        }
        maze_file = Tools.full_name(const.MAZES_DIR, settings.MAZE_FILE)
        try:
            with open(maze_file, 'r') as tileset_file:
                for line_number, line in enumerate(tileset_file):
                    for char_number, char in enumerate(line):
                        structure = "Unknown"
                        for structure_key in const.STRUCTURES:
                            if char == const.STRUCTURES[structure_key]:
                                structure = structure_key
                                break
                        if structure != "Unknown":
                            self.zones[(char_number, line_number-1)] = \
                                structure
                            counters[structure] += 1
        except FileNotFoundError:
            print("The configuration file was not found:", maze_file)
            sys.exit()
        except PermissionError:
            print("You don't have the adequate rights to read the maze file:",
                  maze_file)
            sys.exit()
        else:
            if (len(self.zones) != const.MAZE_WIDTH * const.MAZE_HEIGHT or
                    counters[const.MAZE_START] < 1 or
                    counters[const.MAZE_EXIT] < 1 or
                    counters[const.MAZE_PATH] < 3):
                try:
                    raise RuntimeError("The configuration file is corrupted:",
                                       maze_file)
                except RuntimeError:
                    print("The configuration file is corrupted:", maze_file)
                    sys.exit()

    def location(self, structure):
        '''

        Returns the coordinates of the first specified structure found.

            Args:
                structure (str): The structure which coordinates are needed.

            Returns:
                location (tuples):
                The coordinates of the first specified structure found.
        '''
        for coordinates in self.zones:
            if self.zones[coordinates] == structure:
                location = coordinates
                break
        return location

    def free_paths(self):
        '''Returns the list of coordinates of the paths of the labyrinth.'''
        return [coordinates for coordinates in self.zones
                if self.zones[coordinates] == const.MAZE_PATH]

    def collision_detected(self, location):
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
        return self.zones[location] == const.MAZE_WALL or \
            x_coordinate < const.MAZE_MIN_WIDTH or \
            x_coordinate > const.MAZE_WIDTH - 1 or \
            y_coordinate < const.MAZE_MIN_HEIGHT or \
            y_coordinate > const.MAZE_HEIGHT - 1
