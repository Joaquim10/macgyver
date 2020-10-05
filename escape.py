#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

escape: escape is the main module and contains the class Escape.

Classes:
    Escape: The Escape object runs the game.

Methods:
    command(key): Returns the command corresponding to the keyboard key
    pressed by the player.
    destination(command): Returns the coordinates of the destination
    corresponding to MacGyver's move.
    display_maze_panel(): Update and displays the maze panel.
    update_sprite(origin, destination): Update MacGyver's sprite.
    update_backpack_bar(): Update the backpack bar and the dirty rects.
    update_log_bar(message):
    update_ending_screen(ending, message): Updates the ending screen.
    display_dirty_rects(): display all the altered parts of the screen
    move(destination): Moves MacGyver to destination and perform his actions.
    run(): Runs the game.
"""
import pygame

from const import Const
from maze import Maze
from macgyver import MacGyver
from guardian import Guardian
from items import Items
from cliinterface import CliInterface
from pginterface import PgInterface


class Escape:
    """

    The Escape object initializes and runs the game.

    Args:

    Class attributes:
        dirty_rects (list): List of Rects used to update the altered areas of
        the screen.

    Attributes:
        screen (Surface): The display Surface.
        pgi (PgInterface): The Pygame interface.
        game_status (string): The status of the game.
        maze (Maze): Represents the labyrinth.
        macgyver (MacGyver): Represents MacGyver.
        guardian (Guardian): Represents the Guardian.
        items (Items): Handles with items.
    """
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
        '''

        Returns the command corresponding to the keyboard key pressed by the
        player.

            Args:
                key (int): The key pressed by the player.

            Returns:
                The command corresponding to the keyboard key pressed by the
                player.
        '''
        command = "unknown"
        for kb_command in Const.HOTKEYS:
            if key == Const.HOTKEYS[kb_command]:
                command = kb_command
                break
        return command

    def destination(self, command):
        '''

        Returns the coordinates of the destination corresponding to MacGyver's
        move.

            Args:
                command (string): The command is MacGyver's move action.

            Returns:
                The coordinates of the destination corresponding to MacGyver's
                move.
        '''
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
        '''Update and displays the maze panel.'''
        self.pgi.blit_maze_panel(self.maze, self.macgyver, self.guardian,
                                 self.items)
        self.screen.blit(self.pgi.maze_panel, self.pgi.maze_rect)
        pygame.display.update(self.pgi.maze_rect)

    def update_sprite(self, origin, destination):
        '''

        Update MacGyver's sprite.

        This method blits a path image at the source and destination positions
        in the labyrinth translated to the screen. MacGyver's image is then
        blited at destination position in the labyrinth translated to the
        screen unless game is lost. If game is lost, it's the Guardian's image
        which is blited. The dirty rects are updated for both blits.

            Args:
                origin (tuples): MacGyver's current coordinates in the
                    labyrinth.
                destination (tuples): Coordinates of the destination of
                    MacGyver's move in the labyrinth.
        '''
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
        '''Update the backpack bar and the dirty rects.'''
        self.pgi.blit_backpack_bar(Items.backpack)
        self.screen.blit(self.pgi.backpack_bar, self.pgi.backpack_rect)
        self.dirty_rects.append(self.pgi.backpack_rect)

    def update_log_bar(self, message):
        '''

        Update the log bar with a message and the dirty rects.

            Args:
                message (string): The message to be displayed in the log bar.

        '''
        self.pgi.blit_log_bar(message)
        self.screen.blit(self.pgi.log_bar, self.pgi.log_rect)
        self.dirty_rects.append(self.pgi.log_rect)

    def update_ending_screen(self, ending, message):
        '''
        Updates the ending screen.

        This method clears the log bar and updates the maze panel as
        background with the ending text and message writed on it. The dirty
        rects are updated.

            Args:
                ending (string): The ending text to be displayed.
                message (string): The message to be displayed at the end of
                the ending text.

        '''
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
        """display all the altered parts of the screen"""
        pygame.display.update(self.dirty_rects)
        self.dirty_rects.clear()

    def move(self, destination):
        '''
        Moves MacGyver to destination and perform his actions.

        This method moves Macgyver to his destination.
        If there is an item at destination, MacGyver gets it, and if MacGyver
        has tree items, he crafts the syringe and the other items are lost.
        In theese cases, the back pack bar and the log bar are updated.
        If the Guardian is at destination, the game status is updated.
        The MacGyver's sprite is then updated and the command line interface
        is printed if needed.
        If game is ending, the ending screen is updated and printed on the
        command line interface if needed.

            Args:
                destination (tuples): Coordinates of the destination of
                    MacGyver in the labyrinth.
        '''
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
        '''
        Runs the game.

        This method displays the labyrinth and print the command line
        interface if needed. An event loop is then processed until game is
        over or canceled. On a keydown event, the key pressed gives a command
        who is processed. If the player tries to move and there is no
        collision detected, MacGyver moves to his destination. At last, all
        the altered parts of the screen are displayed.

        '''
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
                            # Display all the altered parts of the screen
                            self.display_dirty_rects()
        if Const.CLI_INTERFACE and self.game_status == "game canceled":
            CliInterface.print_ending(Const.CAPTION,
                                      Const.ENDINGS[self.game_status])


if __name__ == "__main__":
    escape = Escape()
    escape.run()
