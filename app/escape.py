#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""

escape: escape contains the class Escape.

Classes:
    Escape: The Escape object runs the game.

Methods:
    fullscreen(): Returns the pygame flag for the selected fullscreen or
        windowed mode.
    command(key): Returns the command corresponding to the keyboard key
        pressed by the player.
    destination(command): Returns the coordinates of the destination
        corresponding to MacGyver's move.
    display_maze_panel(): Update and displays the maze panel.
    update_sprite(origin, destination): Update MacGyver's sprite.
    update_backpack_bar(): Update the backpack bar and the dirty rects.
    update_log_bar(message): Update the log bar with a message and the dirty
        rects.
    update_ending_screen(ending, message): Updates the ending screen.
    display_dirty_rects(): Display all the altered parts of the screen.
    move(destination): Moves MacGyver to destination and perform his actions.
    run(): Runs the game.
"""

import pygame

import config.settings as settings
import config.const as const
from app.maze import Maze
from app.macgyver import MacGyver
from app.guardian import Guardian
from app.items import Items
from app.clidisplay import CliDisplay
from app.pgimage import PgImage
from app.pginterface import PgInterface


class Escape:
    """

    The Escape object initializes and runs the game.

    Class attributes:
        dirty_rects (list [pygame.Rects]): List of Rects used to update the
        altered areas of the screen.

    Attributes:
        screen (pygame.Surface): The display Surface.
        pgi (pginterface.PgInterface): The Pygame interface.
        game_status (str): The status of the game.
            {"game in progress", "game won", "game lost", "game over",
             "game canceled"}
        maze (maze.Maze): Represents the labyrinth.
        macgyver (macgyver.MacGyver): Represents MacGyver.
        guardian (guardian.Guardian): Represents the Guardian.
        items (items.Items): Handles with items.
    """
    dirty_rects = []

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        # Initialize display
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH,
                                              settings.SCREEN_HEIGHT),
                                              Escape.fullscreen())
        pygame.display.set_caption(settings.CAPTION)
        # Initialize Pygame interface
        self.pgi = PgInterface()
        # Initialize game
        self.game_status = "game in progress"
        tile_size = self.pgi.tile_side, self.pgi.tile_side
        wall_image = PgImage.load_crop(const.TEXTURE_ATLAS,
                                       const.CROP_WALL_POSITION,
                                       const.CROP_SIZE,
                                       tile_size)
        path_image = PgImage.load_crop(const.TEXTURE_ATLAS,
                                       const.CROP_PATH_POSITION,
                                       const.CROP_SIZE,
                                       tile_size)
        self.maze = Maze(wall_image, path_image)
        location = self.maze.location(const.MAZE_START)
        image = PgImage.load(const.MACGYVER_FILE, tile_size)
        self.macgyver = MacGyver(location, image)
        location = self.maze.location(const.MAZE_EXIT)
        image = PgImage.load(const.GUARDIAN_FILE, tile_size)
        self.guardian = Guardian(location, image)
        self.items = Items(self.maze.free_paths(), tile_size)

    @staticmethod
    def fullscreen():
        '''

        Returns the pygame flag for the selected fullscreen or windowed mode.

            Returns:
                fullscreen (int):
                If fullscreen mode is selected, returns the pygame fullscreen
                flag. If windowed mode is selected, returns 0.
        '''
        if settings.FULLSCREEN:
            fullscreen = pygame.FULLSCREEN
        else:
            fullscreen = 0
        return fullscreen

    @staticmethod
    def command(key):
        '''

        Returns the command corresponding to the keyboard key pressed by the
        player.

            Args:
                key (int): The key pressed by the player.

            Returns:
                command (str): The command corresponding to the keyboard key
                pressed by the player.
        '''
        hotkeys = {
            "move left": pygame.K_LEFT,
            "move right": pygame.K_RIGHT,
            "move up": pygame.K_UP,
            "move down": pygame.K_DOWN,
            "exit game": pygame.K_ESCAPE,
            "validate": pygame.K_SPACE
        }
        command = "unknown"
        for kb_command in hotkeys:
            if key == hotkeys[kb_command]:
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
                x_coordinate (tuple), y_coordinate (tuple):
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
        self.pgi.blit_backpack_bar(self.items.backpack)
        self.screen.blit(self.pgi.backpack_bar, self.pgi.backpack_rect)
        self.dirty_rects.append(self.pgi.backpack_rect)

    def update_log_bar(self, message):
        '''

        Update the log bar with a message and the dirty rects.

            Args:
                message (str): The message to be displayed in the log bar.

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
                ending (str): The ending text to be displayed.
                message (str): The message to be displayed at the end of the
                    ending text.

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
        '''Display all the altered parts of the screen.'''
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
        for item in self.items.materials:
            if destination == item.position:
                self.items.pick_up(item)
                if self.items.items_in_backpack >= 3:
                    self.items.craft()
                    message = "MacGyver got {} and crafted {}.".format(
                        item.description, self.items.syringe.description)
                else:
                    message = "MacGyver got {}.".format(item.description)
                self.update_log_bar(message)
                self.update_backpack_bar()
        if destination == self.guardian.position:
            if self.items.syringe in self.items.backpack:
                self.game_status = "game won"
            else:
                self.game_status = "game lost"
        self.update_sprite(origin, destination)
        if settings.CLI_DISPLAY:
            CliDisplay .print_interface(self.maze.zones,
                                        self.macgyver.position,
                                        self.items.backpack,
                                        self.items.materials)
        if self.game_status in ["game won", "game lost"]:
            ending = settings.ENDINGS[self.game_status]
            message = "Press SPACE bar or ESCAPE to quit."
            self.update_ending_screen(ending, message)
            if settings.CLI_DISPLAY:
                CliDisplay .print_ending(settings.CAPTION,
                                         settings.ENDINGS[self.game_status])

    def run(self):
        '''

        Runs the game.

        This method displays the labyrinth and print the command line
        interface if needed. An event loop is then processed until game is
        over or canceled. On a keydown event, the key pressed gives a command
        who is processed. If the player tries to move and there is no
        collision detected, MacGyver moves to his destination. Finally, all
        the altered parts of the screen are displayed.

        '''
        # Display all the maze and all the sprites
        self.display_maze_panel()
        if settings.CLI_DISPLAY:
            CliDisplay .print_interface(self.maze.zones,
                                        self.macgyver.position,
                                        self.items.backpack,
                                        self.items.materials)
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
        if settings.CLI_DISPLAY and self.game_status == "game canceled":
            CliDisplay .print_ending(settings.CAPTION,
                                     settings.ENDINGS[self.game_status])
