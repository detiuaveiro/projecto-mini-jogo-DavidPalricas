import pygame as pg
from entity import Entity
import sound_player as sp
import finite_state_machine as fsm
import os

class Player(Entity):
    """ A class to represent the player in the game
        The player class inherits from the Sprite class
    """
    def __init__(self, grid_size, ground_level): 
        """ Constructor for the Player class
            It calls the constructor of the parent class and initializes the player attributes
            Set the player speed, gravity, jump speed, player_turned_right , is_on_ground and sound_player attributes
        """
        # Construct the absolute path to the sprite image
        sprite_path = os.path.join(os.path.dirname(__file__), "../Assets/SpriteSheets/Bowser/Idle/bowser_idle.png")
        super().__init__(sprite_path, grid_size, ground_level)
    
        self.speed = 1.8
        self.jump_speed = 50
        self.states = self.set_states()
        self.transitions = self.set_transitions()
        self.fsm = fsm.FSM(self.states, self.transitions)
        self.sound_player = sp.SoundPlayer("jump", False)
        self.name = "Bowser"
        self.last_key_pressed = None
    

    def set_states(self):
        """ Method to set the states of the player
            It creates the idle, walk and jump states for the player
            Return the states variable (stores the states of the player)
        """
        self.idle = fsm.Idle()
        self.walk = fsm.Walk()
        self.jump = fsm.Jump()
        return [self.idle, self.walk, self.to_jump]
    

    def set_transitions(self):
        """ Method to set the transitions of the player
            It creates the transitions for the player
            Return the transitions variable (stores the transitions of the player)
        """
        return {
            "walk": fsm.Transition(self.idle, self.walk),
            "jump": fsm.Transition(self.idle, self.jump),
            "idle": fsm.Transition(self.walk, self.idle),
            "fall": fsm.Transition(self.jump, self.idle)
        }
                
    def update(self):
        """ Update the player's position based on the keys pressed """
        pressed_keys = pg.key.get_pressed()
        self.move(pressed_keys)
        
    
    def move(self, keys):
        """ Method to move the player
            If the player is not on the ground, it calls the handling_fall method
            Otherwise, it moves the player based on the key pressed, to the right or to the left, and makes the player jump by calling the jump method
            It also flips the player image based on the direction the player is moving, and if the LSHIFT key is pressed, the player moves faster
            
            Parameters: keys (stores the keys pressed by the player)
        """
        if not self.is_on_ground:
            self.handling_fall()
        else: 
            if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
                self.fsm.update("jump", self)
                self.to_jump()
            elif keys[pg.K_d] or keys[pg.K_RIGHT]:
                self.fsm.update("walk", self)
                self.rect.x += 2 * self.speed if keys[pg.K_LSHIFT] else self.speed
                if not self.turned_right:
                    self.image = pg.transform.flip(self.image, True, False)
                    self.turned_right = True

                self.last_key_pressed = pg.K_d if keys[pg.K_d] else pg.K_RIGHT

            elif keys[pg.K_a] or keys[pg.K_LEFT]:
                self.fsm.update("walk", self)
                self.rect.x -= 2 * self.speed if keys[pg.K_LSHIFT] else self.speed
                if self.turned_right:
                    self.image = pg.transform.flip(self.image, True, False)
                    self.turned_right = False
                
                self.last_key_pressed = pg.K_d if keys[pg.K_d] else pg.K_RIGHT
            
            # Check if the player stopped moving horizontally
            if self.last_key_pressed != None and not keys[self.last_key_pressed]:
                self.fsm.update("idle", self)

    
    def to_jump(self):
        """ Method to make the player jump
            It makes the player jump and plays the jump sound effect
            It also sets the is_on_ground attribute to False
        """
        self.sound_player.play()
        self.is_on_ground = False
        self.rect.y -= self.jump_speed

    def handling_fall(self):
        """ Method to handle the player falling
            It makes the player fall if the player is not on the ground
            When the player reaches the ground, it sets the is_on_ground attribute to True
        """
        if not self.is_on_ground:
            self.rect.y += self.gravity

            if self.rect.y >= self.ground_level - self.grid_size:
                self.fsm.update("fall", self)
                self.rect.y = self.ground_level - self.grid_size
                self.is_on_ground = True