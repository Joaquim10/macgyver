#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

guardian: guardian contains the class Guardian.

Classes:
    Guardian: The Guardian object represents the Guardian.
"""


class Guardian:
    """

    The Guardian object represents the Guardian.

    Args:
        position (tuples): Coordinates of the Guardian in the labyrinth.
        image (pygame.Surface): Image for the Guardian.

    Attributes:
        position (tuples): Coordinates of the Guardian in the labyrinth.
        image (pygame.Surface): Image of the Guardian.
    """
    def __init__(self, position, image):
        self.position = position
        self.image = image
