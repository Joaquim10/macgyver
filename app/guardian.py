#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

guardian: guardian contains the class Guardian.

Classes:
    Guardian: The Guardian object represents the Guardian.
"""

from config.const import MAZE_EXIT
from app.maze import Maze
from app.pgimage import PgImage


class Guardian:
    """

    The Guardian object represents the Guardian.

    Args:
        position (tuples): Coordinates of the Guardian in the labyrinth.
        image_size (tuples): Width and height for the image for the Guardian.

    Attributes:
        position (tuples): Coordinates of the Guardian in the labyrinth.
        image (pygame.Surface): Image of the Guardian.
    """
    def __init__(self, image_size):
        self.position = Maze.location(MAZE_EXIT)
        self.image = PgImage.load("Gardien.png", image_size)
