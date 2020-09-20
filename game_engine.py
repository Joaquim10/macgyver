#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from maze import Maze
from macgyver import MacGyver
from guardian import Guardian
from item import Item
from output_engine import OutputEngine
from input_engine import InputEngine


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
