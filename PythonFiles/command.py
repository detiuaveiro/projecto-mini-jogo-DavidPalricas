import pygame as pg
from command import MoveRightCommand, MoveLeftCommand, JumpCommand, SprintCommand, QuitGameCommand
class Command:
    def execute(self, player):
        pass

class MoveRightCommand(Command):
    def execute(self, player):
        player.move_right()

class MoveLeftCommand(Command):
    def execute(self, player):
        player.move_left()

class JumpCommand(Command):
    def execute(self, player):
        player.initiate_jump()

class SprintCommand(Command):
    def execute(self, player):
        player.sprint()

class QuitGameCommand(Command):
    def execute(self, player):
        player.quit_game()

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
            pg.K_LSHIFT: SprintCommand(),
            pg.K_ESCAPE: QuitGameCommand()
        }

    def set_command(self, key, command):
        self.commands[key] = command

    def handle_input(self, key):
        return self.commands.get(key, None)