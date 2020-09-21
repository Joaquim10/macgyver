#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
from maze import Maze


class Output:

    @staticmethod
    def _clear_console():
        if os.name in ('nt','dos'):
            os.system("cls")
        elif os.name in ('linux','osx','posix'):
            os.system("clear")
        else:
            print("\n" * 120)

    @staticmethod
    def _print_separator(length=40):
        print("~" * length)

    @classmethod
    def print_interface(cls, macgyver, loot, backpack):
        cls._clear_console()
        # Draw maze
        for y_coordinate in range(Maze.MIN_HEIGHT, Maze.MAX_HEIGHT + 1):
            line = ""
            for x_coordinate in range(Maze.MIN_WIDTH, Maze.MAX_WIDTH + 1):
                # Structures
                if (Maze.ZONES[x_coordinate, y_coordinate] == Maze.STRUCTURE_WALL):
                    char = "#"
                elif (Maze.ZONES[x_coordinate, y_coordinate] == Maze.STRUCTURE_PATH):
                    char = " "
                elif (Maze.ZONES[x_coordinate, y_coordinate] == Maze.STRUCTURE_START):
                    char = "?"
                elif (Maze.ZONES[x_coordinate, y_coordinate] == Maze.STRUCTURE_EXIT):
                    char = "!"
                # Special locations
                if (x_coordinate, y_coordinate) == macgyver.position:
                    char = "@" # MacGyver
                else:
                    for item in loot:
                        if item.position == (x_coordinate, y_coordinate):
                            char = "$" # Item
                line += char
            print(line)
        # Print MacGyver current position
        print("Macgyver", macgyver.position)
        # Print counter and items in backpack
        print("Backpack: {} items".format(macgyver.items_in_backpack))
        for item in backpack:
            print("- {}".format(item.name.capitalize()))
        cls._print_separator(17)

    @classmethod
    def print_ending(cls, message, length=40):
        cls._clear_console()
        cls._print_separator(length)
        print("MacGyver".center(length))
        print("(CLI version)".center(length))
        cls._print_separator(length)
        for line in message.split("\n"):
            print(line.center(length))
        cls._print_separator(length)
