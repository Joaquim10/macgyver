#!./env/bin/python python3.7
# -*- coding: UTF-8 -*-

import pygame

from const import Const
from maze import Maze
from macgyver import MacGyver
from guardian import Guardian
from items import Items
from cliinterface import CliInterface
from pginterface import PgInterface


class Escape:

    dirty_rects = []

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        # Initialize display
        self.screen = pygame.display.set_mode((Const.SCREEN_WIDTH,
                                              Const.SCREEN_HEIGHT),
                                              Const.FULLSCREEN)
        pygame.display.set_caption(Const.CAPTION)
        # Initialize Pygame interface
        self.pgi = PgInterface()
        # Initialize game
        self.game_status = "game in progress"
        self.maze = Maze((self.pgi.tile_side, self.pgi.tile_side))
        self.macgyver = MacGyver((self.pgi.tile_side, self.pgi.tile_side))
        self.guardian = Guardian((self.pgi.tile_side, self.pgi.tile_side))
        self.items = Items((self.pgi.tile_side, self.pgi.tile_side))

    @staticmethod
    def command(key):
        command = "unknown"
        for kb_command in Const.HOTKEYS:
            if key == Const.HOTKEYS[kb_command]:
                command = kb_command
                break
        return command

    def destination(self, command):
        x_coordinate, y_coordinate = self.macgyver.position
        if command == "move left":
            x_coordinate -= 1
        elif command == "move right":
            x_coordinate += 1
        elif command == "move up":
            y_coordinate -= 1
        elif command == "move down":
            y_coordinate += 1
        return x_coordinate, y_coordinate

    def display_maze_panel(self):
        self.pgi.blit_maze_panel(self.maze, self.macgyver, self.guardian,
                                 self.items)
        self.screen.blit(self.pgi.maze_panel, self.pgi.maze_rect)
        pygame.display.update(self.pgi.maze_rect)

    def update_sprite(self, origin, destination):
        # Blit a path at origin
        rect = self.pgi.abs_translate(origin)
        self.screen.blit(self.maze.path_image, rect)
        self.dirty_rects.append(rect)
        # Blit a path at destination
        rect = self.pgi.abs_translate(destination)
        self.screen.blit(self.maze.path_image, rect)
        # Blit character at destination
        if self.game_status != "game lost":
            image = self.macgyver.image
        else:
            image = self.guardian.image
        self.screen.blit(image, rect)
        self.dirty_rects.append(rect)

    def update_backpack_bar(self):
        self.pgi.blit_backpack_bar(Items.backpack)
        self.screen.blit(self.pgi.backpack_bar, self.pgi.backpack_rect)
        self.dirty_rects.append(self.pgi.backpack_rect)

    def update_log_bar(self, message):
        self.pgi.blit_log_bar(message)
        self.screen.blit(self.pgi.log_bar, self.pgi.log_rect)
        self.dirty_rects.append(self.pgi.log_rect)

    def update_ending_screen(self, ending, message):
        # Clear logs
        self.pgi.clear_log_bar()
        self.screen.blit(self.pgi.log_bar, self.pgi.log_rect)
        self.dirty_rects.append(self.pgi.log_rect)
        # Display ending screen
        # Update text background
        self.pgi.maze_panel = self.screen.subsurface(self.pgi.maze_rect)
        self.pgi.maze_panel = self.pgi.maze_panel.convert()
        # Blit background and text
        self.pgi.blit_ending_screen(ending, message)
        self.screen.blit(self.pgi.maze_panel, self.pgi.maze_rect)
        self.dirty_rects.append(self.pgi.maze_rect)

    def display_dirty_rects(self):
        # Update all the altered parts of the screen
        pygame.display.update(self.dirty_rects)
        self.dirty_rects.clear()

    def move(self, destination):
        origin = self.macgyver.position
        self.macgyver.move(destination)
        for item in Items.materials:
            if destination == item.position:
                self.items.pick_up(item)
                if self.items.items_in_backpack >= 3:
                    for material in Items.backpack:
                        material.image = self.pgi.redden(material.image)
                    self.items.craft()
                    message = "MacGyver got {} and crafted {}.".format(
                        item.description, self.items.syringe.description)
                else:
                    message = "MacGyver got {}.".format(item.description)
                self.update_log_bar(message)
                self.update_backpack_bar()
        if destination == self.guardian.position:
            if self.items.syringe in Items.backpack:
                self.game_status = "game won"
            else:
                self.game_status = "game lost"
        self.update_sprite(origin, destination)
        if Const.CLI_INTERFACE:
            CliInterface.print_interface(self.macgyver.position,
                                         self.items.items_in_backpack)
        if self.game_status in ["game won", "game lost"]:
            ending = Const.ENDINGS[self.game_status]
            message = "Press SPACE bar or ESCAPE to quit."
            self.update_ending_screen(ending, message)
            if Const.CLI_INTERFACE:
                CliInterface.print_ending(Const.CAPTION,
                                          Const.ENDINGS[self.game_status])

    def run(self):
        # Display all the maze and all the sprites
        self.display_maze_panel()
        if Const.CLI_INTERFACE:
            CliInterface.print_interface(self.macgyver.position,
                                         self.items.items_in_backpack)
        # Event loop
        while self.game_status not in ["game canceled", "game over"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_status = "game canceled"
                elif event.type == pygame.KEYDOWN:
                    command = self.command(event.key)
                    if command == "exit game" and \
                            self.game_status not in ["game won", "game lost"]:
                        self.game_status = "game canceled"
                    elif command in ["exit game", "validate"] and \
                            self.game_status in ["game won", "game lost"]:
                        self.game_status = "game over"
                    elif command.startswith("move") and \
                            self.game_status == "game in progress":
                        destination = self.destination(command)
                        if not self.maze.collision_detected(destination):
                            # MacGyver moves
                            self.move(destination)
                            # Update all the altered parts of the screen
                            self.display_dirty_rects()
        if Const.CLI_INTERFACE and self.game_status == "game canceled":
            CliInterface.print_ending(Const.CAPTION,
                                      Const.ENDINGS[self.game_status])


if __name__ == "__main__":
    escape = Escape()
    escape.run()
