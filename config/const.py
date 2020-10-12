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
# The wall tiles blocks MacGyver.
# MacGyver can move on the paths tiles.
# The start tile is MacGyver's starting position in the labyrinth.
# The exit tile is the exit of the labyrinth and the location of the Guardian.
MAZE_WALL = "wall"
MAZE_PATH = "path"
MAZE_START = "MacGyver"
MAZE_EXIT = "Guardian"
STRUCTURES = {
    MAZE_WALL: "#",
    MAZE_PATH: " ",
    MAZE_START: "!",
    MAZE_EXIT: "?"
}


# The image files.
MACGYVER_FILE = "MacGyver.png"
GUARDIAN_FILE = "Gardien.png"

# The texture atlas.
# The textures of the walls and the paths are obtained by cropping a 20 pixels
# width by 20 pixels height image from a larger image called the texture
# atlas. The position of the crop is the column and the row of the selected
# texture in the texture atlas.
# 0 <= column <= 19, 0 <= row <= 12
TEXTURE_ATLAS = "floor-tiles-20x20.png"
CROP_WALL_POSITION = 7, 11
CROP_PATH_POSITION = 7, 2
CROP_SIZE = 20, 20

# Items which will be dropped across the labyrinth with their name,
# description, image file and quality.
MATERIALS = {
    "needle": {
        "name": "needle",
        "description": "a needle",
        "image_file": "aiguille.png",
        "quality": "material"
    },
    "tube": {
        "name": "tube",
        "description": "a little plastic tube",
        "image_file": "tube_plastique.png",
        "quality": "material"
    },
    "ether": {
        "name": "ether",
        "description": "some ether",
        "image_file": "ether.png",
        "quality": "material"
    }
}

# Items which can be crafted with their name, description, image file and
# quality.
CRAFTS = {
    "syringe": {
        "name": "syringe",
        "description": "an epidermic syringe",
        "image_file": "seringue.png",
        "quality": "craft"
    }
}

# Interface bars sizes, in number of tiles.
# The backpack's bar is for displayind MacGyver carryied items and the log bar
# is for messages concerning the interaction between MacGyver and the items.
BACKPACK_BAR_WIDTH = 1
BACKPACK_BAR_HEIGHT = 4
LOG_BAR_WIDTH = MAZE_WIDTH
LOG_BAR_HEIGHT = 1
