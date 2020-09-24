#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pygame
from maze import Maze
from macgyver import MacGyver
from guardian import Guardian
from items import Items
from output import Output


class Game:
    ENDINGS = {
        "game won" :
            "The guardian bars the exit of the maze.\n"
            "MacGyver sneaks into the shadows and\n"
            "plants his anaesthetic syringe\n"
            "in the guard's neck, who collapses.\n"
            "MacGyver then escape the labyrinth.\n"
            "Well played !",
        "game lost":
            "MacGyver rushes the exit of the maze,\n"
            "but he's killed by the Guardian.\n"
            "Game over !",
        "game canceled":
            "MacGyver is lost in the maze forever.\n"
            "Game over !"
    }

    SCREEN_WIDTH, SCREEN_HEIGHT = 1440, 900
    BLACK = 0, 0, 0

    HOT_KEYS = {
        "move left": pygame.K_LEFT,
        "move right": pygame.K_RIGHT,
        "move up": pygame.K_UP,
        "move down": pygame.K_DOWN,
        "exit game" : pygame.K_ESCAPE
    }

    def __init__(self):
        # initialize display
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('MagGyver - Escape the labyrinth')

        self.game_status = "game in progress"
        self.maze = Maze()
        self.macgyver = MacGyver()
        self.guardian = Guardian()
        self.items = Items()

    @classmethod
    def command(cls, key):
        command = "unknown"
        for kb_command in cls.HOT_KEYS:
            if key == cls.HOT_KEYS[kb_command]:
                command = kb_command
                break
        return command

    @classmethod
    def collision_detected(cls, location):
        x_coordinate, y_coordinate = location
        return (Maze.ZONES[location] == Maze.STRUCTURE_WALL or
        x_coordinate < Maze.MIN_WIDTH  or x_coordinate > Maze.MAX_WIDTH or
        y_coordinate < Maze.MIN_HEIGHT or y_coordinate > Maze.MAX_HEIGHT)

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
        if not self.collision_detected(destination):
            self.macgyver.move(destination) # Move

            for item in Items.LOOT:
                if destination == item.position:
                    self.macgyver.pick_up(item) # Pick up an item
                    Items.LOOT.remove(item)
                    Items.free_paths.append(item.position)
                    if self.macgyver.items_in_backpack >=3: # Craft an item
                        self.macgyver.craft(self.items.syringe)
            if destination == self.guardian.position: # Ending
                if self.items.syringe in Items.BACKPACK:
                    self.game_status = "game won"
                else:
                    self.game_status = "game lost"

    def display_backgroung(self):
        for y_coordinate in range(Maze.MIN_HEIGHT, Maze.HEIGHT):
            for x_coordinate in range(Maze.MIN_WIDTH, Maze.WIDTH):
                if (Maze.ZONES[x_coordinate, y_coordinate] == Maze.STRUCTURE_WALL):
                    self.maze.wall_rect.topleft = (x_coordinate * self.maze.wall_rect.w,
                    y_coordinate * self.maze.wall_rect.h)
                    self.screen.blit(self.maze.wall_image, self.maze.wall_rect)
                else:
                    self.maze.path_rect.topleft = (x_coordinate * self.maze.path_rect.w,
                    y_coordinate * self.maze.path_rect.h)
                    self.screen.blit(self.maze.path_image, self.maze.path_rect)

    def play_game(self):
        Output.print_interface(self.macgyver)
        # Event loop
        while self.game_status == "game in progress":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_status = "game canceled"
                elif event.type == pygame.KEYDOWN:
                    command = self.command(event.key)
                    if command == "exit game":
                        self.game_status = "game canceled"
                    elif command.startswith("move"):
                        self.handle_actions(command)
                        Output.print_interface(self.macgyver)

            # Display on the screen
            self.screen.fill(self.BLACK)
            self.display_backgroung()
            self.screen.blit(self.maze.path_image, self.maze.path_rect)
            self.screen.blit(self.maze.wall_image, self.maze.wall_rect)
            self.screen.blit(self.guardian.image, self.guardian.rect)
            self.screen.blit(self.macgyver.image, self.macgyver.rect)
            pygame.display.flip()

        Output.print_ending(self.ENDINGS[self.game_status]) # Ending


def main():
    game = Game()
    game.play_game()

if __name__ == "__main__":
    main()
