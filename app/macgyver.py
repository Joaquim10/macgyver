#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

macgyver: macgyver contains the class MacGyver.

Classes:
    MacGyver: The MacGyver object represents MacGyver.

Methods:
    move(position): Moves MacGyver in the labyrinth.
"""


class MacGyver():
    """

    The MacGyver object represents MacGyver.

    Args:
        position (tuples): Coordinates of MacGyver in the labyrinth.
        image (pygame.Surface): image for MacGyver.

    Attributes:
        position (tuples): Coordinates of MacGyver in the labyrinth.
        image (pygame.Surface): Image of MacGyver.
    """
    def __init__(self, position, image):
        self.position = position
        self.image = image

    def move(self, position):
        '''

        Moves MacGyver in the labyrinth.

            Args:
                position (tuples): The new coordinates of MacGyver in the
                labyrinth.
        '''
        self.position = position
