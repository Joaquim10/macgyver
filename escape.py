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

    HOT_KEYS = {
        "move left": pygame.K_LEFT,
        "move right": pygame.K_RIGHT,
        "move up": pygame.K_UP,
        "move down": pygame.K_DOWN,
        "exit game" : pygame.K_ESCAPE
    }

    def __init__(self):
        self.game_status = "game in progress"
        # initialize display
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("MagGyver - Escape the labyrinth")
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

    def destination(self, command):
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

    @classmethod
    def collision_detected(cls, location):
        x_coordinate, y_coordinate = location
        return (Maze.zones[location] == Maze.WALL or
        x_coordinate < Maze.MIN_WIDTH  or x_coordinate > Maze.MAX_WIDTH or
        y_coordinate < Maze.MIN_HEIGHT or y_coordinate > Maze.MAX_HEIGHT)

    def move(self, destination):
        self.macgyver.move(destination)
        for item in Items.loot:
            if destination == item.position:
                self.items.pick_up(item)
                if self.items.items_in_backpack >=3:
                    self.items.craft()
        if destination == self.guardian.position:
            if self.items.syringe in Items.backpack:
                self.game_status = "game won"
            else:
                self.game_status = "game lost"

    def display_screen(self):
        # Display background
        for y_coordinate in range(Maze.MIN_HEIGHT, Maze.HEIGHT):
            for x_coordinate in range(Maze.MIN_WIDTH, Maze.WIDTH):
                if (Maze.zones[x_coordinate, y_coordinate] == Maze.WALL):
                    self.maze.wall_rect.topleft = (x_coordinate * self.maze.wall_rect.w,
                    y_coordinate * self.maze.wall_rect.h)
                    self.screen.blit(self.maze.wall_image, self.maze.wall_rect)
                else:
                    self.maze.path_rect.topleft = (x_coordinate * self.maze.path_rect.w,
                    y_coordinate * self.maze.path_rect.h)
                    self.screen.blit(self.maze.path_image, self.maze.path_rect)
        # Display sprites
        for item in self.items.loot:
            self.screen.blit(item.image, item.rect)
        self.screen.blit(self.guardian.image, self.guardian.rect)
        self.screen.blit(self.macgyver.image, self.macgyver.rect)
        pygame.display.flip()

    def play_game(self):
        dirty_rects = []
        self.display_screen()
        #Output.print_interface(self.macgyver.position, self.items.items_in_backpack)
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
                        destination = self.destination(command)
                        if not self.collision_detected(destination):
                            self.screen.blit(self.maze.path_image, self.macgyver.rect)
                            dirty_rects.append(self.macgyver.rect.copy())
                            self.move(destination)
                            self.screen.blit(self.maze.path_image, self.macgyver.rect)
                            self.screen.blit(self.macgyver.image, self.macgyver.rect)
                            dirty_rects.append(self.macgyver.rect)
                            pygame.display.update(dirty_rects)
                            dirty_rects.clear()
                            #Output.print_interface(self.macgyver.position,
                            #self.items.items_in_backpack)
        Output.print_ending(self.ENDINGS[self.game_status]) # Ending


def main():
    game = Game()
    game.play_game()

if __name__ == "__main__":
    main()
