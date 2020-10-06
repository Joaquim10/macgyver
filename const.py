#!/bin/python/env python3
# -*- coding: UTF-8 -*-

class Const:

    # Screen / window
    CAPTION = "MagGyver - Escape the labyrinth"
    SCREEN_WIDTH, SCREEN_HEIGHT = 1440, 900

    # Enable Windowed mode / Fullscreen
    FULLSCREEN = 0  # 0 | pygame.FULLSCREEN

    # Enable / Disable command line interface
    CLI_INTERFACE = False

    # Directories
    RESSOURCE_DIR = "ressource"
    CONFIG_DIR = "config"
    CONFIG_FILE = "maze.txt"

    # Maze tiles
    MAZE_MIN_WIDTH, MAZE_WIDTH = 0, 15
    MAZE_MIN_HEIGHT, MAZE_HEIGHT = 0, 15
    MAZE_WALL = "wall"
    MAZE_PATH = "path"
    MAZE_START = "MacGyver"
    MAZE_EXIT = "Guardian"

    # Images for the maze tiles
    # (0...19, 0...12)
    CROP_WALL_POSITION = 7, 11
    CROP_PATH_POSITION = 7, 2
    CROP_SIZE = 20, 20

    # End of game display
    ENDINGS = {
        "game won":
            "The guardian bars the exit of the maze.\n\n"
            "MacGyver sneaks into the shadows\n"
            "and plants his anaesthetic syringe in\n"
            "the guard's neck, who collapses.\n\n"
            "MacGyver then escape the labyrinth.\n\n"
            "Well played !",
        "game lost":
            "The guardian patrols the labyrinth.\n\n"
            "MacGyver rushes towards the exit,\n"
            "but a fight begins and he is finally\n"
            "killed by the Guardian.\n\n"
            "Game over !",
        "game canceled":
            "MacGyver is lost in the maze forever.\n\n"
            "Game over !"
    }

    # Bars sizes (in number of tiles)
    BACKPACK_BAR_WIDTH = 1
    BACKPACK_BAR_HEIGHT = 4
    LOG_BAR_HEIGHT = 1
