import pygame as pg
from command import MoveRightCommand, MoveLeftCommand, JumpCommand, SprintCommand

class InputHandler:
    def __init__(self):
        self.commands = {
            pg.K_UP: JumpCommand(),
            pg.K_LEFT: MoveLeftCommand(),
            pg.K_RIGHT: MoveRightCommand(),
            pg.K_w: JumpCommand(),
            pg.K_a: MoveLeftCommand(),
            pg.K_d: MoveRightCommand(),
            pg.K_SPACE: JumpCommand(),
            pg.K_LSHIFT: SprintCommand()
        }

    def set_command(self, key, command):
        self.commands[key] = command

    def handle_input(self, key):
        return self.commands.get(key, None)