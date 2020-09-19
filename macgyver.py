#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os


class Maze:

    ZONES = {}
    MIN_WIDTH, MAX_WIDTH = 0, 14
    MIN_HEIGHT, MAX_HEIGHT = 0, 14

    STRUCTURE_WALL = "Wall"
    STRUCTURE_PATH = "Path"
    STRUCTURE_START = "MacGyver"
    STRUCTURE_EXIT = "Guardian"

    @classmethod
    def init_zones(cls):

        structures = {
            cls.STRUCTURE_WALL: "#",
            cls.STRUCTURE_PATH: " ",
            cls.STRUCTURE_START: "?",
            cls.STRUCTURE_EXIT: "!"
        }
        subdirectory = "config"
        configuration_file = "maze.txt"
        working_directory = os.path.dirname(__file__)
        configuration_file = os.path.join(working_directory, subdirectory,
            configuration_file)
        try:
            with open(configuration_file, 'r') as config_file:
                for line_number, line in enumerate(config_file):
                    for char_number, char in enumerate(line):
                        for structure_key in structures:
                            structure = cls.STRUCTURE_PATH
                            if char == structures[structure_key]:
                                structure = structure_key
                                break
                        cls.ZONES[(char_number, line_number - 1)] = structure
        except FileNotFoundError as error:
            print("The configuration file was not found : {}".format(error))
        except Exception as error:
            print("Unexpected error : {} ".format(error))

    @classmethod
    def location(cls, structure):
        for coordinates in cls.ZONES:
            if cls.ZONES[coordinates] == structure:
                location = coordinates
                break
        return location

    @classmethod
    def free_paths(cls):
        return [coordinates for coordinates in cls.ZONES if cls.ZONES[coordinates] ==
            cls.STRUCTURE_PATH]


class MacGyver:

    def __init__(self, position):
        self.position = position


class Guardian:

    def __init__(self, position):
        self.position = position


class Item:

    def __init__(self, name, position):
        self.name = name
        self.position = position


class GameScript:

    def __init__(self):
        Maze.init_zones()
        self.macgyver = MacGyver(Maze.location(Maze.STRUCTURE_START))
        self.guardian = Guardian(Maze.location(Maze.STRUCTURE_EXIT))
        self.free_paths = Maze.free_paths()

if __name__ == "__main__":
    game_script = GameScript()
