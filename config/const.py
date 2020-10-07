#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""const contains the constants definitions"""

# Directory for the graphic ressources.
RESSOURCES_DIR = "../ressources"

# Directory for the labyrinth levels (the tile set grids).
MAZES_DIR = "../mazes"

# Size of labyrinth.
# The labyrinth has a width of 15 zones and an height of 15 zones.
MAZE_MIN_WIDTH, MAZE_WIDTH = 0, 15
MAZE_MIN_HEIGHT, MAZE_HEIGHT = 0, 15

# The structures of the labyrinth.
# The walls blocks MacGyver.
# MacGyver can move on the paths tiles.
# The start tile is where MacGyver starts the level.
# The exit tile is the exit of the labyrinth and where the Guardian is.
MAZE_WALL = "wall"
MAZE_PATH = "path"
MAZE_START = "MacGyver"
MAZE_EXIT = "Guardian"

# The texture atlas.
# The textures of the walls and the paths are obtained by cropping a 20 pixels
# width by 20 pixels height image from a larger image called the texture
# atlas. The position of the crop is the row and the column of the selected
# texture in the texture atlas.
# 0 <= row <= 19, 0 <= column <= 12
TEXTURE_ATLAS = "floor-tiles-20x20.png"
CROP_WALL_POSITION = 7, 11
CROP_PATH_POSITION = 7, 2
CROP_SIZE = 20, 20

# Interface bars sizes (in number of tiles).
# The backpack's bar is for displayind MacGyver carryied items and the log bar
# is for messages concerning the interaction between MacGyver and the items.
BACKPACK_BAR_WIDTH = 1
BACKPACK_BAR_HEIGHT = 4
LOG_BAR_WIDTH = MAZE_WIDTH
LOG_BAR_HEIGHT = 1
