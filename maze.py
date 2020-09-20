#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import random


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
                        structure = cls.STRUCTURE_PATH
                        for structure_key in structures:
                            if char == structures[structure_key]:
                                structure = structure_key
                                break
                        cls.ZONES[(char_number, line_number - 1)] = structure
                        counters[structure] += 1
        except FileNotFoundError as error:
            print("The configuration file was not found.")
            return error
        except PermissionError as error:
            print("You don't have the adequate rights to read the configuration file.")
            return error
        except Exception as error:
            print("Unexpected error.")
            return error
        else:
            if (counters[cls.STRUCTURE_START] < 1 or
                counters[cls.STRUCTURE_EXIT] < 1 or
                counters[cls.STRUCTURE_PATH] < 3):
                try:
                    raise Exception("corrupted configuration file : {}".format(configuration_file))
                except Exception as error:
                    return error
            else:
                return None

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

    @classmethod
    def random_location(cls, locations):
        free_location = False
        while not free_location:
            coordinates = (random.randrange(cls.MIN_WIDTH, cls.MAX_WIDTH),
                random.randrange(cls.MIN_HEIGHT, cls.MAX_HEIGHT))
            if coordinates in locations:
                free_location = True
        return coordinates

    @classmethod
    def collision_detected(cls, location):
        x_coordinate, y_coordinate = location
        return (cls.ZONES[location] == cls.STRUCTURE_WALL or
            x_coordinate < cls.MIN_WIDTH  or x_coordinate > cls.MAX_WIDTH or
            y_coordinate < cls.MIN_HEIGHT or y_coordinate > cls.MAX_HEIGHT)
