#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

pginterface: pginterface contains the class PgInterface.

Classes:
    PgImnterface: The PgInterface object initializes and blits panels and
    bars.

Methods:
    translate(position):
        Translates the specified position in the labyrinth to the relative
        coordinates in a surface.
    abs_translate(position):
        Translates the specified position in the labyrinth to the
        corresponding rect in the display surface.
    blit_maze_panel(maze, macgyver, guardian, items):
        Blits the maze panel with all walls, paths, items and caracters images.
    blit_backpack_bar(backpack):
        Blits the backpack bar with all MacGyver's carryed items images.
    clear_log_bar():
        Clears the log bar.
    blit_log_bar(message):
        Blits the log bar with a message.
    blit_ending_screen(ending, message):
        Darken and blits the maze panel with the ending text followed by a
        message with different colors.
    redden(image):
        Redden and return a surface.
"""

import pygame

import config.settings as settings
import config.const as const
from app.maze import Maze


class PgInterface:
    """

    The PgInterface object initializes and blits panels and bars.

    Attributes:
        tile_side (int): The width or height of the squared tiles.
        maze_panel (pygame.Surface) : The maze panel surface.
        maze_rect (pygame.Rect) : The maze panel rect.
        backpack_bar (pygame.Surface) : The backpack bar surface.
        self.backpack_rect (pygame.Rect) : The backpack bar rect.
        log_bar (pygame.Surface) : The log bar surface.
        log_rect (pygame.Rect) : The log bar rect.
    """
    def __init__(self):
        # Initialize tiles size
        self.tile_side = self._tile_side()
        # Initialize interface
        self.maze_panel, self.maze_rect = self._maze_panel()
        self.backpack_bar, self.backpack_rect = self._backpack_bar()
        self.log_bar, self.log_rect = self._log_bar()

    @staticmethod
    def _tile_side():
        '''Returns the side of the squared tiles witch best fits the display
        surface.'''
        return min(settings.SCREEN_WIDTH // (const.MAZE_WIDTH +
                                             const.BACKPACK_BAR_WIDTH * 2),
                   settings.SCREEN_HEIGHT // (const.MAZE_HEIGHT +
                                              const.LOG_BAR_HEIGHT))

    def _maze_panel(self):
        '''Returns the maze panel surface and rect witch best fits the display
        surface.'''
        width = const.MAZE_WIDTH * self.tile_side
        height = const.MAZE_HEIGHT * self.tile_side
        x_coordinate = (settings.SCREEN_WIDTH - width) // 2
        y_coordinate = (settings.SCREEN_HEIGHT - height) // 2 - \
            self.tile_side // 2
        maze_panel = pygame.Surface((width, height)).convert()
        maze_rect = pygame.Rect(x_coordinate, y_coordinate, width, height)
        return maze_panel, maze_rect

    def _backpack_bar(self):
        '''Returns the backpack bar surface and rect witch best fits the
        display surface.'''
        width = self.tile_side * const.BACKPACK_BAR_WIDTH
        height = self.tile_side * const.BACKPACK_BAR_HEIGHT
        x_coordinate = self.maze_rect.x - self.tile_side - 1
        y_coordinate = self.maze_rect.bottom - height
        backpack_panel = pygame.Surface((width, height)).convert()
        backpack_rect = pygame.Rect(x_coordinate, y_coordinate, width, height)
        return backpack_panel, backpack_rect

    def _log_bar(self):
        '''Returns the log bar surface and rect witch best fits the display
        surface.'''
        width = self.tile_side * const.LOG_BAR_WIDTH
        height = self.tile_side * const.LOG_BAR_HEIGHT
        x_coordinate = (settings.SCREEN_WIDTH - width) // 2
        y_coordinate = self.maze_rect.bottom + 1
        log_bar = pygame.Surface((width, height)).convert()
        log_rect = pygame.Rect(x_coordinate, y_coordinate, width, height)
        return log_bar, log_rect

    def translate(self, position):
        '''

        Translates the specified position in the labyrinth to the relative
        coordinates in a surface.

            Args:
                position (tuples): The coordinates of the position in the
                labyrinth.

            Returns:
                x_coordinate (tuple), y_coordinate (tuple):
                The relative coordinates of the position in a surface.
        '''
        x_coordinate, y_coordinate = position
        x_coordinate *= self.tile_side
        y_coordinate *= self.tile_side
        return x_coordinate, y_coordinate

    def abs_translate(self, position):
        '''

        Translates the specified position in the labyrinth to the
        corresponding rect in the display surface.

            Args:
                position (tuples): The coordinates of the position in the
                labyrinth.

            Returns:
                rect (pygame.Rect)
                The rect in the display surface cooresponding to the specified
                position in the labyrinth.
        '''
        position = self.translate(position)
        rect = pygame.Rect(position, (self.tile_side, self.tile_side))
        return rect.move(self.maze_rect.x, self.maze_rect.y)

    def blit_maze_panel(self, maze, macgyver, guardian, items):
        '''

        Blits the maze panel with all walls, paths, items and caracters
        images.

            Args:
                maze (maze.Maze): The maze object.
                macgyver (macgyver.MacGyver): MacGyver object.
                guardian (guardian.Guardian): Guardian object.
                items (items.Items): Item object.
        '''
        # Blit the maze background
        for y_coordinate in range(const.MAZE_MIN_HEIGHT, const.MAZE_HEIGHT):
            for x_coordinate in range(const.MAZE_MIN_WIDTH, const.MAZE_WIDTH):
                position = self.translate((x_coordinate, y_coordinate))
                if Maze.zones[x_coordinate, y_coordinate] == const.MAZE_WALL:
                    self.maze_panel.blit(maze.wall_image, position)
                else:
                    self.maze_panel.blit(maze.path_image, position)
        # Display sprites
        for item in items.materials:
            self.maze_panel.blit(item.image, self.translate(item.position))
        self.maze_panel.blit(guardian.image, self.translate(guardian.position))
        self.maze_panel.blit(macgyver.image, self.translate(macgyver.position))

    def blit_backpack_bar(self, backpack):
        '''

        Blits the backpack bar with all MacGyver's carryed items images.

            Args:
                backpack (list [items.Items]):
                The list of items to blit their images.
        '''
        x_coordinate, y_coordinate = 0, 0
        for item in backpack:
            self.backpack_bar.blit(item.image, (x_coordinate, y_coordinate))
            y_coordinate += self.tile_side

    def clear_log_bar(self):
        '''Clears the log bar.'''
        self.log_bar.fill(pygame.Color("black"))

    def blit_log_bar(self, message):
        '''

        Blits the log bar with a message.

            Args:
                message (str): the message to be blited.
        '''
        self.clear_log_bar()
        font = pygame.font.SysFont('Arial', self.tile_side // 2)
        message_surface = font.render(message, True, pygame.Color("white"))
        message_rect = message_surface.get_rect()
        message_rect.y = self.tile_side // 5
        self.log_bar.blit(message_surface, message_rect)

    def _blit_ending(self, text, y_position, font,
                     color=pygame.Color("white")):
        '''

        Blits the maze panel with horizontally centered multi-line text.
           Automatic line feed is not supported.

            Args:
                text (str) : The text to be blited.
                y_position (int) : The y_axis coordinate in the maze panel
                for the beginning of the text.

            Returns:
                y_position (int):
                The y_axis coordinate in the maze panel for the text position
                at the end of the blitting.
        '''
        lines = text.splitlines()
        for line in lines:
            line_surface = font.render(line, True, color)
            line_rect = line_surface.get_rect()
            line_rect.x = (self.maze_rect.width - line_rect.width) // 2
            line_rect.y = y_position
            self.maze_panel.blit(line_surface, line_rect)
            y_position += line_rect.height
        y_position += line_rect.height
        return y_position

    def blit_ending_screen(self, ending, message):
        '''

        Darken and blits the maze panel with the ending text followed by a
        message with different colors.

            Args:
                ending (str) : The text to be first blited.
                message (str) : The text to be blited after the ending.
        '''
        self.maze_panel.fill(pygame.Color("gray10"), None, pygame.BLEND_SUB)
        font = pygame.font.SysFont('Arial', self.tile_side * 5 // 6)
        ending += "\n\n"
        text_position = self.tile_side * 2
        text_position = self._blit_ending(ending, text_position, font,
                                          pygame.Color("white"))
        text_position = self._blit_ending(message, text_position, font,
                                          pygame.Color("orange"))

    @staticmethod
    def redden(image):
        '''

        Redden and return a surface.
            Args:
                image (pygame.Surface) : The image to be redden.

            Returns:
                image (pygame.Surface)
                The reddened image.
        '''
        image.fill(pygame.Color("cyan"), None, pygame.BLEND_SUB)
        return image
