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