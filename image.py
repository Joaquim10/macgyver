#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys

import pygame

from const import Const


class Image:

    @staticmethod
    def _full_name(file_name):
        working_directory = os.path.dirname(__file__)
        return os.path.join(working_directory, Const.RESSOURCE_DIR, file_name)

    @staticmethod
    def _load(image_file):
        """ Load image and return image object"""
        try:
            image = pygame.image.load(image_file)
        except pygame.error:
            print('Cannot load image:', image_file)
            sys.exit()
        else:
            return image

    @staticmethod
    def _scale(image, size):
        image = pygame.transform.scale(image, size)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        return image

    @classmethod
    def load(cls, image_file, scale_size):
        image_file = cls._full_name(image_file)
        image = cls._load(image_file)
        image = cls._scale(image, scale_size)
        return image

    @classmethod
    def load_crop(cls, image_file, crop_position, crop_size, scale_size):
        image_file = cls._full_name(image_file)
        crop_x, crop_y = crop_position
        crop_width, crop_height = crop_size
        crop_rect = crop_x * crop_width, crop_y * crop_height, \
            crop_width, crop_height
        image = cls._load(image_file)
        image = image.subsurface(crop_rect)
        image = cls._scale(image, scale_size)
        return image
