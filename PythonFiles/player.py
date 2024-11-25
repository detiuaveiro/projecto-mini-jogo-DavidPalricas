import os
import pygame as pg
from entity import Entity
import sound_player as sp
import finite_state_machine as fsm

class Player(Entity):
    """
    The Player class is responsible for managing the player entity in the game world.
    
    The class has the following attributes:
        - jump_speed: The speed of the player's jump
        - sound_player: The sound player of the player
        - last_key_pressed: The last key pressed by the player
        - game_map: The game map
    """
    def __init__(self, grid_size, ground_level, game_map): 
        """
        Initializes a new instance of the Player class, and calls the constructor of the Entity class (the parent class).
        Loads the sprite image for the player.
        Sets up the player's attributes and the attributes inherited from the Entity class including the FSM and its states.

        Args:
            - grid_size (int): The size of the grid in the game world
            - ground_level (int): The level of the ground in the game world
            - game_map (GameMap): The game map
        """
        sprite_path = os.path.join(os.path.dirname(__file__), "../Assets/SpriteSheets/Bowser/Idle/bowser_idle.png")
        super().__init__(sprite_path, grid_size, ground_level)

        # Set up the player's attributes
        self.jump_speed = 15  
        self.sound_player = sp.SoundPlayer("jump", False)
        self.last_key_pressed = None
        self.game_map = game_map

        # Set up the attributes inherited from the Entity class
        self.speed = 1.8
        self.gravity = 1
        self.is_on_ground = True
        self.turned_right = True
        self.name = "Bowser"

        # Initialize FSM and states
        self.fsm = fsm.FSM(self.set_states(), self.set_transitions())

        # Set the player's initial position on the ground
        self.rect.x = 0
        self.rect.bottom = ground_level

    def set_states(self):
        """
        Sets up the states for the FSM.
        
        :return: A dictionary of states.
        """
        states = {
            "idle": self.idle_state,
            "jump": self.jump_state,
            "walk": self.walk_state,
        }
        return states

    def set_transitions(self):
        """
        Sets up the transitions for the FSM.
        
        :return: A dictionary of transitions.
        """
        transitions = {
            "idle_to_jump": ("idle", "jump"),
            "jump_to_idle": ("jump", "idle"),
            "idle_to_walk": ("idle", "walk"),
            "walk_to_idle": ("walk", "idle"),
        }
        return transitions

    def idle_state(self):
        """
        The idle state of the player.
        """
        pass

    def jump_state(self):
        """
        The jump state of the player.
        """
        pass

    def walk_state(self):
        """
        The walk state of the player.
        """
        pass

    def update(self):
        """
        Updates the player's state and position.
        """
        self.fsm.update()
        self.apply_gravity()
        self.move()

    def apply_gravity(self):
        """
        Applies gravity to the player.
        """
        if not self.is_on_ground:
            self.rect.y += self.gravity

    def move(self):
        """
        Moves the player based on input.
        """
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rect.x -= self.speed
            self.turned_right = False
        if keys[pg.K_RIGHT]:
            self.rect.x += self.speed
            self.turned_right = True
        if keys[pg.K_SPACE] and self.is_on_ground:
            self.rect.y -= self.jump_speed
            self.is_on_ground = False
            self.sound_player.play()

    def draw(self, window):
        """
        Draws the player on the window.
        
        :param window: The game window surface.
        """
        window.blit(self.image, self.rect)