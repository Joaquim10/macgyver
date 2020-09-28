#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import pygame


class Image:

    WIDTH, HEIGHT = 20, 20

    @classmethod
    def load(cls, file_name):
        """ Load image and return image object"""
        subdirectory = "ressource"
        working_directory = os.path.dirname(__file__)
        full_name = os.path.join(working_directory, subdirectory, file_name)
        try:
            image = pygame.image.load(full_name)
            image = pygame.transform.scale(image, (cls.WIDTH, cls.HEIGHT))
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except pygame.error:
            print('Cannot load image:', full_name)
            sys.exit()
        else:
            return image, image.get_rect()

    @classmethod
    def load_crop(cls, file_name, position, width, height):
        subdirectory = "ressource"
        working_directory = os.path.dirname(__file__)
        full_name = os.path.join(working_directory, subdirectory, file_name)
        x_coordinate, y_coordinate = position
        rect = x_coordinate * width, y_coordinate * height, width, height
        try:
            image = pygame.image.load(full_name)
            image = image.subsurface(rect)
            image = pygame.transform.scale(image, (cls.WIDTH, cls.HEIGHT))
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except pygame.error:
            print('Cannot load image:', full_name)
            sys.exit()
        else:
            return image, image.get_rect()
