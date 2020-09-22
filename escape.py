#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from maze import Maze
from macgyver import MacGyver
from guardian import Guardian
from item import Item
from output import Output
from controller import Controller


class Game:

    ENDINGS = {
        "game won" :
            "The guardian bars the exit of the maze.\n"
            "MacGyver sneaks into the shadows and\n"
            "plants his anaesthetic syringe\n"
            "in the guard's neck, who collapses.\n"
            "MacGyver then leaves the labyrinth.\n"
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
        self.error = Maze.init_zones()
        if not self.error:
            self.game_status = "game in progress"
            self.macgyver = MacGyver(Maze.location(Maze.STRUCTURE_START))
            self.guardian = Guardian(Maze.location(Maze.STRUCTURE_EXIT))
            self.free_paths = Maze.free_paths()
            self.syringe = Item("syringe", self.macgyver.position)
            # Drop items on random free paths
            self.loot = []
            for item_name in ["needle", "tube", "ether"]:
                location = Maze.random_location(self.free_paths)
                self.loot.append(Item(item_name, location))
                self.free_paths.remove(location)
        else:
            self.game_status = "game error"

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
                if destination == item.position:
                    self.macgyver.pick_up(item) # Pick up an item
                    self.loot.remove(item)
                    self.free_paths.append(item.position)
                    if self.macgyver.items_in_backpack >=3: # Craft an item
                        Output.print_interface(self.macgyver, self.loot, self.macgyver.backpack)
                        input("MacGyver is crafting a syringe...\n")
                        self.macgyver.craft(self.syringe)
            if destination == self.guardian.position: # Ending
                if self.syringe in self.macgyver.backpack:
                    self.game_status = "game won"
                else:
                    self.game_status = "game lost"

    def play_game(self):
        while self.game_status == "game in progress":
            Output.print_interface(self.macgyver, self.loot, self.macgyver.backpack)
            command = Controller.command("Direction ? ")
            if Controller.is_move(command):
                self.handle_actions(command)
            elif command == "exit":
                self.game_status = "game canceled"
        if self.game_status != "game error": # Ending
            Output.print_ending(self.ENDINGS[self.game_status])
        else:
            print(self.error)


def main():
    game = Game()
    game.play_game()

if __name__ == "__main__":
    main()
