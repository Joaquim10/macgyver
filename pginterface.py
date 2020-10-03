#!./env/bin/python python3.7
# -*- coding: UTF-8 -*-

import pygame

from const import Const
from maze import Maze


class PgInterface:

    def __init__(self):
        # Initialize tiles size
        self.tile_side = self._tile_side()
        # Initialize interface
        self.maze_panel, self.maze_rect = self._maze_panel()
        self.backpack_bar, self.backpack_rect = self._backpack_bar()
        self.log_bar, self.log_rect = self._log_bar()

    @staticmethod
    def _tile_side():
        return min(Const.SCREEN_WIDTH // (Const.MAZE_WIDTH +
                   Const.BACKPACK_BAR_WIDTH * 2),
                   Const.SCREEN_HEIGHT // (Const.MAZE_HEIGHT +
                   Const.LOG_BAR_HEIGHT))

    def _maze_panel(self):
        width = Const.MAZE_WIDTH * self.tile_side
        height = Const.MAZE_HEIGHT * self.tile_side
        x_coordinate = (Const.SCREEN_WIDTH - width) // 2
        y_coordinate = (Const.SCREEN_HEIGHT - height) // 2 - \
            self.tile_side // 2
        maze_panel = pygame.Surface((width, height)).convert()
        maze_rect = pygame.Rect(x_coordinate, y_coordinate, width, height)
        return maze_panel, maze_rect

    def _backpack_bar(self):
        width = self.tile_side * Const.BACKPACK_BAR_WIDTH
        height = self.tile_side * Const.BACKPACK_BAR_HEIGHT
        x_coordinate = self.maze_rect.x - self.tile_side - 1
        y_coordinate = self.maze_rect.bottom - height
        backpack_panel = pygame.Surface((width, height)).convert()
        backpack_rect = pygame.Rect(x_coordinate, y_coordinate, width, height)
        return backpack_panel, backpack_rect

    def _log_bar(self):
        width = Const.MAZE_WIDTH * self.tile_side
        height = self.tile_side * Const.LOG_BAR_HEIGHT
        x_coordinate = (Const.SCREEN_WIDTH - width) // 2
        y_coordinate = self.maze_rect.bottom + 1
        log_bar = pygame.Surface((width, height)).convert()
        log_rect = pygame.Rect(x_coordinate, y_coordinate, width, height)
        return log_bar, log_rect

    def translate(self, position):
        x_coordinate, y_coordinate = position
        x_coordinate *= self.tile_side
        y_coordinate *= self.tile_side
        return x_coordinate, y_coordinate

    def abs_translate(self, position):
        position = self.translate(position)
        rect = pygame.Rect(position, (self.tile_side, self.tile_side))
        return rect.move(self.maze_rect.x, self.maze_rect.y)

    def blit_maze_panel(self, maze, macgyver, guardian, items):
        # Display maze background
        for y_coordinate in range(Const.MAZE_MIN_HEIGHT, Const.MAZE_HEIGHT):
            for x_coordinate in range(Const.MAZE_MIN_WIDTH, Const.MAZE_WIDTH):
                position = self.translate((x_coordinate, y_coordinate))
                if Maze.zones[x_coordinate, y_coordinate] == Const.MAZE_WALL:
                    self.maze_panel.blit(maze.wall_image, position)
                else:
                    self.maze_panel.blit(maze.path_image, position)
        # Display sprites
        for item in items.materials:
            self.maze_panel.blit(item.image, self.translate(item.position))
        self.maze_panel.blit(guardian.image, self.translate(guardian.position))
        self.maze_panel.blit(macgyver.image, self.translate(macgyver.position))

    def blit_backpack_bar(self, backpack):
        x_coordinate, y_coordinate = 0, 0
        for item in backpack:
            self.backpack_bar.blit(item.image, (x_coordinate, y_coordinate))
            y_coordinate += self.tile_side

    def clear_log_bar(self):
        self.log_bar.fill(pygame.Color("black"))

    def blit_log_bar(self, message):
        self.clear_log_bar()
        font = pygame.font.SysFont('Arial', self.tile_side // 2)
        message_surface = font.render(message, True, pygame.Color("white"))
        message_rect = message_surface.get_rect()
        message_rect.y = self.tile_side // 5
        self.log_bar.blit(message_surface, message_rect)

    def _blit_ending(self, text, y_position, font,
                     color=pygame.Color("white")):
        """blit maze image horizontally centered multi-line text
           (without automatic line feed)"""
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
        image.fill(pygame.Color("cyan"), None, pygame.BLEND_SUB)
        return image
