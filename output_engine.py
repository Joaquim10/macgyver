#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
from maze import Maze


class OutputEngine:

    @staticmethod
    def clear_console():
        if os.name in ('nt','dos'):
            os.system("cls")
        elif os.name in ('linux','osx','posix'):
            os.system("clear")
        else:
            print("\n" * 120)

    @staticmethod
    def print_separator(length=40):
        print("~" * length)

    @classmethod
    def print_interface(cls, macgyver, loot, backpack):
        cls.clear_console()
        # Draw maze
        for y_coordinate in range(Maze.MIN_HEIGHT, Maze.MAX_HEIGHT+1):
            line = ""
            for x_coordinate in range(Maze.MIN_WIDTH, Maze.MAX_WIDTH+1):
                # Structures
                if (Maze.ZONES[x_coordinate, y_coordinate] ==
                        Maze.STRUCTURE_WALL):
                    char = "#"
                elif (Maze.ZONES[x_coordinate, y_coordinate] ==
                        Maze.STRUCTURE_PATH):
                    char = " "
                elif (Maze.ZONES[x_coordinate, y_coordinate] ==
                        Maze.STRUCTURE_START):
                    char = "?"
                elif (Maze.ZONES[x_coordinate, y_coordinate] ==
                        Maze.STRUCTURE_EXIT):
                    char = "!"
                # Special locations
                if (x_coordinate, y_coordinate) == macgyver.position:
                    char = "@"
                else:
                    for item in loot:
                        if item.position == (x_coordinate, y_coordinate):
                            char = "$"
                line += char
            print(line)
        # Print MacGyver current position
        print("Macgyver", macgyver.position)
        # Print backpack items
        print("Backpack: {} items".format(macgyver.items_in_backpack))
        for item in backpack:
            print("- {}".format(item.name.capitalize()))
        cls.print_separator(17)

    @classmethod
    def print_ending(cls, message, length=40):
        OutputEngine.clear_console()
        OutputEngine.print_separator(length)
        print("MacGyver".center(length))
        print("(CLI version)".center(length))
        OutputEngine.print_separator(length)
        for line in message.split("\n"):
            print(line.center(length))
        OutputEngine.print_separator(length)

