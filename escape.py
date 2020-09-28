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
    SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 1000
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

    def __init__(self):
        # Initialize display
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(self.CAPTION)
        # Initialize scaled images
        Image.WIDTH = Image.HEIGHT = min(self.SCREEN_WIDTH // (Maze.WIDTH + 2),
            self.SCREEN_HEIGHT // (Maze.HEIGHT + 1))
        # Initialize screen centered maze area
        self.maze_area = pygame.Surface((0, 0))
        self.maze_rect = pygame.Rect(0, 0, 0, 0)
        self.set_maze_area()
        # Initialize backpack area
        self.backpack_area = pygame.Surface((0, 0))
        self.backpack_rect = pygame.Rect(0, 0, 0, 0)
        self.set_backpack_area()
        # Initialize message area
        self.message_area = pygame.Surface((0, 0))
        self.message_rect = pygame.Rect(0, 0, 0, 0)
        self.set_message_area()
        # Initialize game
        self.dirty_rects = []
        self.maze = Maze()
        self.macgyver = MacGyver()
        self.guardian = Guardian()
        self.items = Items()

    def set_maze_area(self):
        width = Maze.WIDTH * Image.WIDTH
        height = Maze.HEIGHT * Image.HEIGHT
        x_coordinate = (self.SCREEN_WIDTH - width) // 2
        y_coordinate = (self.SCREEN_HEIGHT - height) // 2 - Image.HEIGHT // 2
        self.maze_area = pygame.Surface((width, height)).convert()
        self.maze_rect = pygame.Rect(x_coordinate, y_coordinate, width, height)

    def set_backpack_area(self):
        width = Image.WIDTH
        height = Image.HEIGHT * 4
        x_coordinate = self.maze_rect.x - Image.WIDTH - 1
        y_coordinate = self.maze_rect.bottom - height
        self.backpack_area = pygame.Surface((width, height)).convert()
        self.backpack_rect = pygame.Rect(x_coordinate, y_coordinate, width, height)

    def set_message_area(self):
        width = Maze.WIDTH * Image.WIDTH
        height = Image.HEIGHT
        x_coordinate = (self.SCREEN_WIDTH - width) // 2
        y_coordinate = self.maze_rect.bottom + 1
        self.message_area = pygame.Surface((width, height)).convert()
        self.message_rect = pygame.Rect(x_coordinate, y_coordinate, width, height)

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
                    for material in Items.backpack:
                        material.image.fill((0, 255, 255), None, pygame.BLEND_SUB)
                    self.items.craft()
                    message = "MacGyver got {} and he crafted {}.".format(
                        item.description, self.items.syringe.description)
                else:
                    message = "MacGyver got {}.".format(item.description)
                font = pygame.font.SysFont('Arial', Image.WIDTH // 2)
                self.blit_message(message, font, pygame.Color("white"))
                self.dirty_rects.append(self.message_rect)
                self.blit_backpack()
                self.dirty_rects.append(self.backpack_rect)
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
        self.screen.blit(self.maze_area, self.maze_rect)

    def blit_backpack(self):
        x_coordinate, y_coordinate = self.backpack_rect.topleft
        for item in Items.backpack:
            self.screen.blit(item.image, (x_coordinate, y_coordinate))
            y_coordinate += Image.HEIGHT

    def blit_text(self, text, y_position, font, color=pygame.Color("white")):
        """ blit maze area horizontally centered multi-line text (without automatic line feed) """
        lines = text.splitlines()
        for line in lines:
            line_surface = font.render(line, True, color)
            line_rect = line_surface.get_rect()
            line_rect.x = (self.maze_rect.width - line_rect.width) // 2
            line_rect.y = y_position
            self.maze_area.blit(line_surface, line_rect)
            y_position += line_rect.height
        y_position += line_rect.height
        return y_position

    def blit_message(self, text, font, color=pygame.Color("white")):
        self.message_area.fill(pygame.Color("black"))
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.x = (self.message_rect.width - text_rect.width) // 2
        text_rect.y = Image.HEIGHT // 5
        self.message_area.blit(text_surface, text_rect)
        self.screen.blit(self.message_area, self.message_rect)

    def play_game(self):
        game_status = "game in progress"
        self.blit_maze_area()
        pygame.display.update(self.maze_rect)
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
                            self.dirty_rects.append(self.macgyver.rect.move(
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
                            self.dirty_rects.append(self.macgyver.rect.move(
                                self.maze_rect.x, self.maze_rect.y))
                            pygame.display.update(self.dirty_rects)
                            self.dirty_rects.clear()

                            #Output.print_interface(self.macgyver.position, self.items.items_in_backpack)
                            if game_status in ["game won", "game lost"]:
                                # Clear_message
                                self.message_area.fill(pygame.Color("black"))
                                self.screen.blit(self.message_area, self.message_rect)
                                # Display screen centered ending
                                self.maze_area = self.screen.subsurface(self.maze_rect).convert()
                                font = pygame.font.SysFont('Arial', Image.WIDTH * 5 // 6)
                                ending = (self.ENDINGS[game_status] + "\n\n")
                                message = "Press SPACE or ESCAPE to quit."
                                text_position = Image.HEIGHT * 2
                                text_position = self.blit_text(ending, text_position,
                                font, pygame.Color("white"))
                                text_position = self.blit_text(message, text_position,
                                    font, pygame.Color("orange"))
                                self.screen.blit(self.maze_area, self.maze_rect)
                                pygame.display.update(self.maze_rect)
                                Output.print_ending(self.ENDINGS[game_status])
        # Game is over
        if game_status == "game canceled":
            Output.print_ending(self.ENDINGS[game_status])

def main():
    game = Game()
    game.play_game()

if __name__ == "__main__":
    main()
