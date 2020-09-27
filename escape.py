#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pygame
from maze import Maze
from macgyver import MacGyver
from guardian import Guardian
from items import Items
from output import Output
from image import Image

class Game:
    SCREEN_WIDTH, SCREEN_HEIGHT = 1440, 900
    CAPTION = "MagGyver - Escape the labyrinth"

    HOTKEYS = {
        "move left": pygame.K_LEFT,
        "move right": pygame.K_RIGHT,
        "move up": pygame.K_UP,
        "move down": pygame.K_DOWN,
        "exit game": pygame.K_ESCAPE,
        "ok": pygame.K_SPACE
    }

    ENDINGS = {
        "game won" :
            "The guardian bars the exit of the maze.\n\n"
            "MacGyver sneaks into the shadows\n"
            "and plants his anaesthetic syringe\n"
            "in the guard's neck, who collapses.\n\n"
            "MacGyver then escape the labyrinth.\n\n"
            "Well played !",
        "game lost":
            "MacGyver rushes the exit of the maze,\n"
            "but he's killed by the Guardian.\n\n"
            "Game over !",
        "game canceled":
            "MacGyver is lost in the maze forever.\n\n"
            "Game over !"
    }

    def __init__(self):
        # Initialize display
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(self.CAPTION)
        # Initialize scaled images
        Image.WIDTH = Image.HEIGHT = min(self.SCREEN_WIDTH // Maze.WIDTH,
            self.SCREEN_HEIGHT // Maze.HEIGHT)
        # Initialize screen centered maze area
        self.maze_area, self.maze_rect = self.maze_area()
        # Initialize game
        self.maze = Maze()
        self.macgyver = MacGyver()
        self.guardian = Guardian()
        self.items = Items()

    def maze_area(self):
        width = Maze.WIDTH * Image.WIDTH
        height = Maze.HEIGHT * Image.HEIGHT
        x_coordinate = (self.SCREEN_WIDTH - width) // 2
        y_coordinate = (self.SCREEN_HEIGHT - height) // 2
        maze_rect = pygame.Rect(x_coordinate, y_coordinate, width, height)
        maze_area = self.screen.subsurface(maze_rect).convert()
        return maze_area, maze_rect

    @classmethod
    def command(cls, key):
        command = "unknown"
        for kb_command in cls.HOTKEYS:
            if key == cls.HOTKEYS[kb_command]:
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
        game_status = "game in progress"
        self.macgyver.move(destination)
        for item in Items.loot:
            if destination == item.position:
                self.items.pick_up(item)
                if self.items.items_in_backpack >=3:
                    self.items.craft()
        if destination == self.guardian.position:
            if self.items.syringe in Items.backpack:
                game_status = "game won"
            else:
                game_status = "game lost"
        return game_status

    def blit_maze_area(self):
        # Display maze background
        for y_coordinate in range(Maze.MIN_HEIGHT, Maze.HEIGHT):
            for x_coordinate in range(Maze.MIN_WIDTH, Maze.WIDTH):
                if (Maze.zones[x_coordinate, y_coordinate] == Maze.WALL):
                    self.maze.wall_rect.x = x_coordinate * self.maze.wall_rect.width
                    self.maze.wall_rect.y = y_coordinate * self.maze.wall_rect.height
                    self.maze_area.blit(self.maze.wall_image, self.maze.wall_rect)
                else:
                    self.maze.path_rect.x = x_coordinate * self.maze.path_rect.width
                    self.maze.path_rect.y = y_coordinate * self.maze.path_rect.height
                    self.maze_area.blit(self.maze.path_image, self.maze.path_rect)
        # Display sprites
        for item in self.items.loot:
            self.maze_area.blit(item.image, item.rect)
        self.maze_area.blit(self.guardian.image, self.guardian.rect)
        self.maze_area.blit(self.macgyver.image, self.macgyver.rect)

    def blit_ending(self, ending, position, font, color=pygame.Color("white")):
        # 2D array where each row is a list of words
        words = [word.split(' ') for word in ending.splitlines()]
        space_width = font.size(' ')[0]
        x_coordinate, y_coordinate = position
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x_coordinate + word_width >= self.maze_rect.right - position[0]:
                    x_coordinate = position[0]  # New line
                    y_coordinate += word_height
                self.maze_area.blit(word_surface, (x_coordinate, y_coordinate))
                x_coordinate += word_width + space_width
            x_coordinate = position[0]  # New line
            y_coordinate += word_height

    def blit_message(self, message, y_position, font, color=pygame.Color("white")):
        message_surface = font.render(message, 0, color)
        message_rect = message_surface.get_rect()
        message_rect.x = (self.maze_rect.width - message_rect.width) // 2
        message_rect.y = self.maze_rect.bottom - message_rect.height - y_position
        self.maze_area.blit(message_surface, message_rect)


    def play_game(self):
        game_status = "game in progress"
        dirty_rects = []
        self.blit_maze_area()
        self.screen.blit(self.maze_area, self.maze_rect)
        pygame.display.flip()
        #Output.print_interface(self.macgyver.position, self.items.items_in_backpack)
        # Event loop
        while game_status not in ["game canceled", "game over"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_status = "game canceled"
                elif event.type == pygame.KEYDOWN:
                    command = self.command(event.key)
                    if (command == "exit game" and game_status != "game won" and
                    game_status != "game lost"):
                        game_status = "game canceled"
                    if command in ["exit game", "ok"] and game_status in ["game won", "game lost"]:
                        game_status = "game over"
                    elif command.startswith("move") and game_status == "game in progress":
                        destination = self.destination(command)
                        if not self.collision_detected(destination):
                            # MacGyver moves
                            self.screen.blit(self.maze.path_image, self.macgyver.rect.move(
                                self.maze_rect.x, self.maze_rect.y))
                            dirty_rects.append(self.macgyver.rect.move(
                                self.maze_rect.x, self.maze_rect.y))
                            game_status = self.move(destination)
                            self.screen.blit(self.maze.path_image, self.macgyver.rect.move(
                                self.maze_rect.x, self.maze_rect.y))
                            if game_status == "game lost":
                                self.screen.blit(self.guardian.image, self.macgyver.rect.move(
                                    self.maze_rect.x, self.maze_rect.y))
                            else:
                                self.screen.blit(self.macgyver.image, self.macgyver.rect.move(
                                    self.maze_rect.x, self.maze_rect.y))
                            dirty_rects.append(self.macgyver.rect.move(
                                self.maze_rect.x, self.maze_rect.y))
                            pygame.display.update(dirty_rects)
                            dirty_rects.clear()
                            #Output.print_interface(self.macgyver.position, self.items.items_in_backpack)
                            if game_status in ["game won", "game lost"]:
                                # Display screen centered ending
                                self.maze_area = self.screen.subsurface(self.maze_rect).convert()
                                font = pygame.font.SysFont('Arial', Image.WIDTH * 5 // 6)
                                ending = (self.ENDINGS[game_status] + "\n\n")
                                message = "Press SPACE or ESCAPE to quit."
                                self.blit_ending(ending, (Image.WIDTH // 2, Image.HEIGHT),
                                    font, pygame.Color('white'))
                                self.blit_message(message, Image.HEIGHT * 2, font,
                                    pygame.Color("orange"))
                                self.screen.blit(self.maze_area, self.maze_rect)
                                pygame.display.flip()
                                Output.print_ending(self.ENDINGS[game_status])
        # Game is over
        if game_status == "game canceled":
            Output.print_ending(self.ENDINGS[game_status])

def main():
    game = Game()
    game.play_game()

if __name__ == "__main__":
    main()
