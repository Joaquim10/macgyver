#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Controller:

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
