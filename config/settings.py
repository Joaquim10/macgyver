#!/bin/python/env python3
# -*- coding: UTF-8 -*-
"""settings contains the settings definitions"""

# Width and height of the screen, in pixels
SCREEN_WIDTH, SCREEN_HEIGHT = 1440, 900

# If FULLSCREEN is set to True, the game will be displayed in fullscreen mode.
# If FULLSCREEN is set to False, the game will be displayed in windowed mode.
FULLSCREEN = False

# If CLI_DISPLAY is set to True, the display of the game in the console is
# activated.
# If CLI_DISPLAY is set to False, the display of the game in the console is
# disabled.
CLI_DISPLAY = True

# The maze structure is stored in a text file.
# It's a grid of 15 characters width and 15 characters height.
# Structures notation in the text file:
# '#' for walls. The wall tiles blocks MacGyver.
# ' ' blank spaces for paths. MacGyver can move on the paths tiles.
# '?' for the player's starting position.
# '!' for the exit of the labyrinth and the location of the guard.
MAZE_FILE = "maze.txt"

# The caption is displayed in windowed mode, and in the ending screen in the
# console if CLI_DISPLAY is enabled.
CAPTION = "MagGyver - Escape the labyrinth"

# Ending screen.
# This is the ending texts when game is won, lost and canceled.
# The game canceled text appears only in the console when CLI_DISPLAY is
# enabled.
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
