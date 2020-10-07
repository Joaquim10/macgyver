#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

clidisplay : clidisplay contains the class CliDisplay .

Classes:
    CliDisplay : The CliDisplay  prints the game interface on the console.
Methods:
    print_interface(macgyver_position, items_in_backpack):
        Prints the game interface on the console.
    print_ending(cls, caption, ending, length=40):
        Print centered caption and ending text.
"""

import os

import config.const as const
from app.maze import Maze
from app.items import Items


class CliDisplay :
    """The CliDisplay  prints the game interface on the console"""

    @staticmethod
    def _clear_console():
        '''Clears the console on any OS. '''
        if os.name in ("nt", "dos"):
            os.system("cls")
        elif os.name in ("linux", "osx", "posix"):
            os.system("clear")
        else:
            print("\n" * 120)

    @staticmethod
    def _print_separator(length=40):
        '''Prints a separator of the specified length.'''
        print("~" * length)

    @classmethod
    def print_interface(cls, macgyver_position, items_in_backpack):
        '''

        Prints the game interface on the command line interface.

        Clears the console and prints all the maze structures, the characters
        and the dropped items. Then prints the number of items carryed by
        MacGyver and justifyed carryed items and quality followed by a
        separator.

            Args:
                caption (str): The text to be printed first.
                ending (str): The text to be printed after the caption.
                length (int, optional): The length is used to center the text
                    and print separators. By default, length is 40.
        '''
        cls._clear_console()
        items_header = "Backpack - {} item(s):".format(items_in_backpack)
        length = len(items_header)
        # Draw maze
        for y_coordinate in range(const.MAZE_MIN_HEIGHT, const.MAZE_HEIGHT):
            line = ""
            for x_coordinate in range(const.MAZE_MIN_WIDTH, const.MAZE_WIDTH):
                # Structures
                if (Maze.zones[x_coordinate, y_coordinate] ==
                        const.MAZE_WALL):
                    char = "#"
                elif (Maze.zones[x_coordinate, y_coordinate] ==
                      const.MAZE_PATH):
                    char = " "
                elif (Maze.zones[x_coordinate, y_coordinate] ==
                      const.MAZE_START):
                    char = "?"
                elif (Maze.zones[x_coordinate, y_coordinate] ==
                      const.MAZE_EXIT):
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
        '''

        Print centered caption and ending text.

            Args:
                caption (str): The text to be printed first.
                ending (str): The text to be printed after the caption.
                length (int, optional): The length is used to center the text
                    and print separators. By default, length is 40.
        '''
        cls._print_separator(length)
        print(caption.center(length))
        cls._print_separator(length)
        for line in ending.split("\n"):
            print(line.center(length))
        cls._print_separator(length)
