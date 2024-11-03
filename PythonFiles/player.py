import pygame as pg
from entity import Entity
import sound_player as sp
import finite_state_machine as fsm
import os

class Player(Entity):
    """A class to represent the player in the game, inheriting from Entity."""

    def __init__(self, grid_size, ground_level, game_map): 
        """Constructor for the Player class.
        
        Initializes the player's image, movement attributes, and finite state machine for managing states.
        """
        sprite_path = os.path.join(os.path.dirname(__file__), "../Assets/SpriteSheets/Bowser/Idle/bowser_idle.png")
        super().__init__(sprite_path, grid_size, ground_level)
    
        self.speed = 1.8
        self.jump_speed = 15  # Adjusted for smoother jumps
        self.gravity = 1
        self.is_on_ground = True
        self.turned_right = True
        self.sound_player = sp.SoundPlayer("jump", False)
        self.name = "Bowser"
        self.last_key_pressed = None
        self.game_map = game_map

        # Initialize FSM and states
        self.states = self.set_states()
        self.transitions = self.set_transitions()
        self.fsm = fsm.FSM(self.states, self.transitions)
        
    def set_states(self):
        """Set the FSM states for the player."""
        self.idle = fsm.Idle()
        self.walk = fsm.Walk()
        self.jump = fsm.Jump()
        return [self.idle, self.walk, self.jump]
    
    def set_transitions(self):
        """Define transitions between player states."""
        return {
            "walk": fsm.Transition(self.idle, self.walk),
            "jump": fsm.Transition(self.idle, self.jump),
            "idle": fsm.Transition(self.walk, self.idle),
            "fall": fsm.Transition(self.jump, self.idle)
        }
                
    def update(self):
        """Update the player's position based on key inputs."""
        pressed_keys = pg.key.get_pressed()
        self.move(pressed_keys)

        if not self.is_on_ground:
         self.apply_gravity()

        self.animator.play_animation(self.fsm.current.name, self)


    def move(self, keys):
        """Move the player based on pressed keys."""
        if not self.is_on_ground:
            self.apply_gravity()
        else: 
            if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
                self.initiate_jump()
            elif keys[pg.K_d] or keys[pg.K_RIGHT]:
                self.move_right(keys)
            elif keys[pg.K_a] or keys[pg.K_LEFT]:
                self.move_left(keys)
            
            # Transition to idle state if no horizontal movement key is pressed
            if self.last_key_pressed and not keys[self.last_key_pressed]:
                self.fsm.update("idle", self)
                self.last_key_pressed = None

    def move_right(self, keys):
        """Move player to the right, handling sprint and sprite flip."""

        if self.fsm.current != self.walk:
            self.fsm.update("walk", self)

        self.rect.x += 2 * self.speed if keys[pg.K_LSHIFT] else self.speed

        if not self.turned_right:
            self.image = pg.transform.flip(self.image, True, False)
            self.turned_right = True

        self.last_key_pressed = pg.K_d if keys[pg.K_d] else pg.K_RIGHT

    def move_left(self, keys):
        """Move player to the left, handling sprint and sprite flip."""  
        
        if self.fsm.current != self.walk:
            self.fsm.update("walk", self)
            
        self.rect.x -= 2 * self.speed if keys[pg.K_LSHIFT] else self.speed

        if self.turned_right:
            self.image = pg.transform.flip(self.image, True, False)
            self.turned_right = False

        self.last_key_pressed = pg.K_a if keys[pg.K_a] else pg.K_LEFT

    def initiate_jump(self):
        """Initiate the jump action, setting state and playing sound."""
        if self.is_on_ground:
            self.fsm.update("jump", self)
            self.sound_player.play()
            self.is_on_ground = False
            self.velocity_y = -self.jump_speed

    def apply_gravity(self):
        """Apply gravity to simulate falling."""
 
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Check if player lands on the ground
        if self.rect.bottom >= self.ground_level:
            self.rect.bottom = self.ground_level
            self.is_on_ground = True
            self.velocity_y = 0
            self.fsm.update("fall", self)
            