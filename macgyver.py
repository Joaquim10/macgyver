#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

macgyver: macgyver contains the class MacGyver.

Classes:
    MacGyver: The MacGyver object represents MacGyver.

Methods:
    move(position): Moves MacGyver in the labyrinth.
"""

from const import Const
from maze import Maze
from pgimage import PgImage


class MacGyver():
    """

    The MacGyver object represents MacGyver.

    Args:
        position (tuples): Coordinates of MacGyver in the labyrinth.
        image_size (tuples): Width and height for the image for MacGyver.

    Attributes:
        position (tuples): Coordinates of MacGyver in the labyrinth.
        image (pygame.Surface): Image of MacGyver.
    """
    def __init__(self, image_size):
        self.position = Maze.location(Const.MAZE_START)
        self.image = PgImage.load("MacGyver.png", image_size)

    def move(self, position):
        '''

        Moves MacGyver in the labyrinth.

            Args:
                position (tuples): The new coordinates of MacGyver in the
                labyrinth.
        '''
        self.position = position
