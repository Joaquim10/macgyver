#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

pgimage: pgimage contains the class PgImage.

Classes:
    PgImage: PgImage handles with images.

Methods:
    load(image_file, scale_size):
        Gets the full name of an image file name and loads, scales, convert
            and returns the corresponding Surface object.
    load_crop(image_file, crop_position, crop_size, scale_size):
        Gets the full name of an image file name and loads, crops, scales,
            convert and returns the corresponding Surface object.
"""

import sys

import pygame

from config.const import RESSOURCES_DIR
from app.tools import Tools


class PgImage:
    """PgImage handles with images."""

    @staticmethod
    def _load(image_file):
        '''Loads an image and returns a Surface object.'''
        try:
            image = pygame.image.load(image_file)
        except pygame.error:
            print('Cannot load image:', image_file)
            sys.exit()
        else:
            return image

    @staticmethod
    def _scale(image, size):
        '''Scales and convert a Surface object.'''
        image = pygame.transform.scale(image, size)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        return image

    @classmethod
    def load(cls, image_file, scale_size):
        '''

        Gets the full name of an image file name and loads, scales, convert
        and returns the corresponding Surface object.

            Args:
                image_file (str): The image file name.
                scale_size (tuples): The width and height for scaling the
                    image.

            Returns:
                image (pygame.Surface)
                The loaded from file, scaled and converted Surface object.
        '''
        image_file = Tools.full_name(RESSOURCES_DIR, image_file)
        image = cls._load(image_file)
        image = cls._scale(image, scale_size)
        return image

    @classmethod
    def load_crop(cls, image_file, crop_position, crop_size, scale_size):
        '''

        Gets the full name of an image file name and loads, crops, scales,
        convert and returns the corresponding Surface object.

            Args:
                image_file (str): The image file name.
                crop_position (tuples): The row and column of the crop.
                    The row and column have a minimum of 0.
                crop_size (tuples): The width and height of the crop.
                scale_size (tuples): The width and height for scaling the
                    image.

            Returns:
                image (pygame.Surface)
                The loaded from file, croped, scaled and converted Surface
                object.
        '''
        image_file = Tools.full_name(RESSOURCES_DIR, image_file)
        crop_x, crop_y = crop_position
        crop_width, crop_height = crop_size
        crop_rect = crop_x * crop_width, crop_y * crop_height, \
            crop_width, crop_height
        image = cls._load(image_file)
        image = image.subsurface(crop_rect)
        image = cls._scale(image, scale_size)
        return image
