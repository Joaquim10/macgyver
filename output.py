#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
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
    def print_interface(cls, macgyver_position, items_in_backpack, length=40):
        cls._clear_console()
        # Draw maze
        for y_coordinate in range(Maze.MIN_HEIGHT, Maze.HEIGHT):
            line = ""
            for x_coordinate in range(Maze.MIN_WIDTH, Maze.WIDTH):
                # Structures
                if (Maze.zones[x_coordinate, y_coordinate] == Maze.WALL):
                    char = "#"
                elif (Maze.zones[x_coordinate, y_coordinate] == Maze.PATH):
                    char = " "
                elif (Maze.zones[x_coordinate, y_coordinate] == Maze.START):
                    char = "?"
                elif (Maze.zones[x_coordinate, y_coordinate] == Maze.EXIT):
                    char = "!"
                # Special locations
                if (x_coordinate, y_coordinate) == macgyver_position:
                    char = "@"
                else:
                    for item in Items.loot:
                        if item.position == (x_coordinate, y_coordinate):
                            char = "$"
                line += char
            print(line.center(length))
        cls._print_separator(length)
        # Print MacGyver current position and counter and items in backpack
        left_column = "Backpack - {} item(s):".format(items_in_backpack)
        length_column = len(left_column)
        right_column = "Macgyver {}".format(macgyver_position).rjust(
            length - length_column)
        print("{}{}".format(left_column, right_column))
        for item in Items.backpack:
            left_column = "- {}".format(item.name.capitalize())
            right_column = "[{}]".format(item.quality).rjust(
                length_column - len(left_column))
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
