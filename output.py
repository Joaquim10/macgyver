#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os

from const import Const
from maze import Maze
from items import Items


class Output:

    @staticmethod
    def _clear_console():
        if os.name in ("nt", "dos"):
            os.system("cls")
        elif os.name in ("linux", "osx", "posix"):
            os.system("clear")
        else:
            print("\n" * 120)

    @staticmethod
    def _print_separator(length=40):
        print("~" * length)

    @classmethod
    def print_interface(cls, macgyver_position, items_in_backpack):
        cls._clear_console()
        items_header = "Backpack - {} item(s):".format(items_in_backpack)
        length = len(items_header)
        # Draw maze
        for y_coordinate in range(Const.MAZE_MIN_HEIGHT, Const.MAZE_HEIGHT):
            line = ""
            for x_coordinate in range(Const.MAZE_MIN_WIDTH, Const.MAZE_WIDTH):
                # Structures
                if (Maze.zones[x_coordinate, y_coordinate] == Const.MAZE_WALL):
                    char = "#"
                elif (Maze.zones[x_coordinate, y_coordinate] ==
                      Const.MAZE_PATH):
                    char = " "
                elif (Maze.zones[x_coordinate, y_coordinate] ==
                      Const.MAZE_START):
                    char = "?"
                elif (Maze.zones[x_coordinate, y_coordinate] ==
                      Const.MAZE_EXIT):
                    char = "!"
                # Special locations
                if (x_coordinate, y_coordinate) == macgyver_position:
                    char = "@"
                else:
                    for item in Items.materials:
                        if item.position == (x_coordinate, y_coordinate):
                            char = "$"
                line += char
            print(line.center(length))
        cls._print_separator(length)
        # Print items counter and items in backpack
        print(items_header)
        for item in Items.backpack:
            left_column = "-{}".format(item.name.capitalize())
            right_column = "[{}]".format(item.quality).rjust(
                length - len(left_column) - 1)
            print("{}{}".format(left_column, right_column))
        cls._print_separator(length)

    @classmethod
    def print_ending(cls, caption, ending, length=40):
        cls._print_separator(length)
        print(caption.center(length))
        cls._print_separator(length)
        for line in ending.split("\n"):
            print(line.center(length))
        cls._print_separator(length)
