#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import random


class Maze:

    ZONES = {}
    MIN_WIDTH, MAX_WIDTH = 0, 14
    MIN_HEIGHT, MAX_HEIGHT = 0, 14

    STRUCTURE_WALL = "Wall"
    STRUCTURE_PATH = "Path"
    STRUCTURE_START = "MacGyver"
    STRUCTURE_EXIT = "Guardian"

    @classmethod
    def init_zones(cls):

        structures = {
            cls.STRUCTURE_WALL: "#",
            cls.STRUCTURE_PATH: " ",
            cls.STRUCTURE_START: "?",
            cls.STRUCTURE_EXIT: "!"
        }
        subdirectory = "config"
        configuration_file = "maze.txt"
        working_directory = os.path.dirname(__file__)
        configuration_file = os.path.join(working_directory, subdirectory,
            configuration_file)
        try:
            with open(configuration_file, 'r') as config_file:
                for line_number, line in enumerate(config_file):
                    for char_number, char in enumerate(line):
                        for structure_key in structures:
                            structure = cls.STRUCTURE_PATH
                            if char == structures[structure_key]:
                                structure = structure_key
                                break
                        cls.ZONES[(char_number, line_number - 1)] = structure
        except FileNotFoundError as error:
            print("The configuration file was not found : {}".format(error))
        except Exception as error:
            print("Unexpected error : {} ".format(error))

    @classmethod
    def location(cls, structure):
        for coordinates in cls.ZONES:
            if cls.ZONES[coordinates] == structure:
                location = coordinates
                break
        return location

    @classmethod
    def free_paths(cls):
        return [coordinates for coordinates in cls.ZONES if cls.ZONES[coordinates] ==
            cls.STRUCTURE_PATH]

    @classmethod
    def random_location(cls, locations):
        free_location = False
        while not free_location:
            coordinates = (random.randrange(cls.MIN_WIDTH, cls.MAX_WIDTH),
            random.randrange(cls.MIN_HEIGHT, cls.MAX_HEIGHT))
            if coordinates in locations:
                free_location = True
        return coordinates

    @classmethod
    def collision_detected(cls, location):
        x_coordinate, y_coordinate = location
        return (cls.ZONES[location] == cls.STRUCTURE_WALL or
            x_coordinate < cls.MIN_WIDTH  or x_coordinate > cls.MAX_WIDTH or
            y_coordinate < cls.MIN_HEIGHT or y_coordinate > cls.MAX_HEIGHT)


class MacGyver:

    def __init__(self, position):
        self.position = position
        self.items_in_backpack = 0

    def move(self, position):
        self.position = position

    def pick_up_item(self):
        self.items_in_backpack += 1

    def craft_item(self):
        return self.items_in_backpack >= 3


class Guardian:

    def __init__(self, position):
        self.position = position


class Item:

    def __init__(self, name, position):
        self.name = name
        self.position = position


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class OutputEngine:

    @staticmethod
    def clear_console():
        if os.name in ('nt','dos'):
            os.system("cls")
        elif os.name in ('linux','osx','posix'):
            os.system("clear")
        else:
            print("\n" * 120)

    @staticmethod
    def print_separator(length=40):
        print("~" * length)

    @classmethod
    def print_interface(cls, macgyver, loot, backpack):
        cls.clear_console()
        # Draw maze
        for y_coordinate in range(Maze.MIN_HEIGHT, Maze.MAX_HEIGHT+1):
            line = ""
            for x_coordinate in range(Maze.MIN_WIDTH, Maze.MAX_WIDTH+1):
                # Structures
                if (Maze.ZONES[x_coordinate, y_coordinate] ==
                        Maze.STRUCTURE_WALL):
                    char = "#"
                elif (Maze.ZONES[x_coordinate, y_coordinate] ==
                        Maze.STRUCTURE_PATH):
                    char = " "
                elif (Maze.ZONES[x_coordinate, y_coordinate] ==
                        Maze.STRUCTURE_START):
                    char = "?"
                elif (Maze.ZONES[x_coordinate, y_coordinate] ==
                        Maze.STRUCTURE_EXIT):
                    char = "!"
                # Special locations
                if (x_coordinate, y_coordinate) == macgyver.position:
                    char = "@"
                else:
                    for item in loot:
                        if item.position == (x_coordinate, y_coordinate):
                            char = "$"
                line += char
            print(line)
        # Print MacGyver current position
        print("Macgyver", macgyver.position)
        # Print backpack items
        print("Backpack: {} items".format(macgyver.items_in_backpack))
        for item in backpack:
            print("- {}".format(item.name.capitalize()))
        cls.print_separator(17)

    @classmethod
    def print_ending(cls, message, length=40):
        OutputEngine.clear_console()
        OutputEngine.print_separator(length)
        print("MacGyver".center(length))
        print("(CLI version)".center(length))
        OutputEngine.print_separator(length)
        for line in message.split("\n"):
            print(line.center(length))
        OutputEngine.print_separator(length)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class InputEngine:

    HOT_KEYS = {
        "move left": "Q", "move right": "D", "move up": "Z", "move down": "S",
        "exit" : "X"
    }

    @classmethod
    def command(cls, prompt=""):
        key = input(prompt)
        if key != "":
            key = key[0].upper()
        command = "unknown"
        for kb_command in cls.HOT_KEYS:
            if key == cls.HOT_KEYS[kb_command]:
                command = kb_command
                break
        return command

    @staticmethod
    def is_move(command):
        return command.startswith("move")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class GameEngine:

    ENDINGS = {
        "game won" :
            "MacGyver crafts an anaesthetic syringe.\n"
            "Then, he sneaks up to the Guardian\n"
            "and puts him to sleep.\n"
            "Finally, he runs away\n"
            "from the labyrinth.\n"
            "Well played !",
        "game lost":
            "MacGyver rushes the exit of the maze,\n"
            "but he's killed by the Guardian.\n"
            "Game over !",
        "game canceled":
            "MacGyver is lost in the maze forever.\n"
            "Game over !"
    }

    def __init__(self):
        Maze.init_zones()
        self.macgyver = MacGyver(Maze.location(Maze.STRUCTURE_START))
        self.guardian = Guardian(Maze.location(Maze.STRUCTURE_EXIT))
        self.free_paths = Maze.free_paths()
        self.game_status = "game in progress"
        self.backpack = []
        self.loot = [] # Drop items on random free paths
        for item_name in ["needle", "tube", "ether"]:
            location = Maze.random_location(self.free_paths)
            self.loot.append(Item(item_name, location))
            self.free_paths.remove(location)

    def handle_actions(self, command):
        x_coordinate, y_coordinate = self.macgyver.position
        if command == "move left":
            x_coordinate -= 1
        elif command == "move right":
            x_coordinate += 1
        elif command == "move up":
            y_coordinate -= 1
        elif command == "move down":
            y_coordinate += 1
        destination = x_coordinate, y_coordinate
        if not Maze.collision_detected(destination):
            self.macgyver.move(destination) # Move
            for item in self.loot:
                if destination == item.position: # Pick up item
                    self.macgyver.pick_up_item()
                    self.backpack.append(item)
                    self.loot.remove(item)
                    self.free_paths.append(item.position)
            if destination == self.guardian.position: # Ending
                if self.macgyver.craft_item():
                    self.game_status = "game won"
                else:
                    self.game_status = "game lost"

    def play_game(self):
        while self.game_status == "game in progress":
            OutputEngine.print_interface(self.macgyver, self.loot,
                self.backpack)
            command = InputEngine.command("Direction ? ")
            if InputEngine.is_move(command):
                self.handle_actions(command)
            elif command == "exit":
                self.game_status = "game canceled"
        OutputEngine.print_ending(self.ENDINGS[self.game_status])

if __name__ == "__main__":
    game_engine = GameEngine()
    game_engine.play_game()
