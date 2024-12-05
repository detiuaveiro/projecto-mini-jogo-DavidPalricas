import pygame as pg
from entity import Entity
import finite_state_machine as fsm
import os

class Player(Entity):
    """
        The Player class is responsible for managing the player entity in the game world
       
        The class has the following attributes:
            - jump_speed: The speed of the player's jump
            - sound_player: The sound player of the player
            - last_key_pressed: The last key pressed by the player
    """

    def __init__(self, collider): 
        """
            Initializes a new instance of the Player class, and calls the constructor of the Entity class (the parent class)
            Loads the sprite image for the player
            Sets up the player's attributes and the attributes inherited from the Entity class including the FSM and its states

            Args:
                - collider (tuple): The collider of the player
        """

        sprite_path = os.path.join(os.path.dirname(__file__), "../Assets/SpriteSheets/Bowser/Idle/bowser_idle.png")
        super().__init__(sprite_path, collider)
         
        self.head_collider = pg.Rect((self.rect.x + 20, self.rect.y - 20, 5, 20))
        # Set up the player's attributes
        self.jump_speed = 15  
        self.last_key_pressed = None

        # Set up the atrributes inherited from the Entity class
        self.speed = 1.8
        self.gravity = 1
        self.is_on_ground = True
        self.turned_right = True
        self.name = "Bowser"

        # Initialize FSM and states
        self.fsm = fsm.FSM(self.set_states(), self.set_transitions())

    def set_states(self):
        """ The set_states method is responsible for setting the states of the player e.g. (idle, walk, jump)
            Returns:
                - states (list): A list of the player's states
        """
        self.idle = fsm.Idle()
        self.walk = fsm.Walk()
        self.jump = fsm.Jump()

        return [self.idle, self.walk, self.jump]
    
    def set_transitions(self):
        """ The set_transitions method is responsible for setting the transitions between the player's states

            Returns:
                - transitions (dict): A dictionary of the player's transitions
        """
        return {
            "walk": fsm.Transition(self.idle, self.walk),
            "jump": fsm.Transition(self.idle, self.jump),
            "idle": fsm.Transition(self.walk, self.idle),
            "fall": fsm.Transition(self.jump, self.idle)
        }
                
    def update(self):
        """ The update method is responsible for move the player based on pressed keys, applying gravity, and playing animations
           Calling respectively this methods: move, apply_gravity, play_animation (from the animator attribute)
        """
        pressed_keys = pg.key.get_pressed()
    
        if not self.is_on_ground:
            self.apply_gravity()
        else: 
            self.move(pressed_keys)

        self.animator.play_animation(self.fsm.current.name, self )


        self.head_collider = pg.Rect((self.rect.x + 20, self.rect.y, 10, 10)) if self.turned_right else pg.Rect((self.rect.x, self.rect.y, 10, 10)) 

   


    def move(self, keys):
        """ The move method is responsible for moving the player based on the pressed keys and sets the player idle if the previous movement key is  released
            If the player presses the space key, W key, or UP key, the initiate_jump method is called to make the player jump
            If the player presses the D key or RIGHT key, the move_right method is called to move the player to the right
            If the player presses the A key or LEFT key, the move_left method is called to move the player to the left

            Args:
                - keys (list): A list of the pressed keys
        """

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
        """ The move_right method is responsible for moving the player to the right, handling sprint and sprite flip.
            It also updates the last_key_pressed attribute to the key pressed and updates the player's state to walk if it's not already in that state

            Args:
             - keys (list): A list of the pressed keys
        """
        
        self.last_key_pressed = pg.K_d if keys[pg.K_d] else pg.K_RIGHT

        if self.fsm.current != self.walk:
            self.fsm.update("walk", self)

        self.rect.x += 2 * self.speed if keys[pg.K_LSHIFT] else self.speed

        if not self.turned_right:
            self.image = pg.transform.flip(self.image, True, False)
            self.turned_right = True


    def move_left(self, keys):
        """ The move_left method is responsible for moving the player to the left, handling sprint and sprite flip.
            It also updates the last_key_pressed attribute to the key pressed and updates the player's state to walk if it's not already in that state

            Args:
                - keys (list): A list of the pressed keys
        """
        
        self.last_key_pressed = pg.K_a if keys[pg.K_a] else pg.K_LEFT

        if self.fsm.current != self.walk:
            self.fsm.update("walk", self)
            
        self.rect.x -= 2 * self.speed if keys[pg.K_LSHIFT] else self.speed

        if self.turned_right:
            self.image = pg.transform.flip(self.image, True, False)
            self.turned_right = False


    def initiate_jump(self):
        """ The initiate_jump method is responsible for making the player jump if it is on the ground.
            It also updates the player's state to jump and plays the jump sound effect.
        """
  
        if self.is_on_ground:
            self.fsm.update("jump", self)
            self.is_on_ground = False
            self.velocity_y = -self.jump_speed


     
    def apply_gravity(self):
        """ The apply_gravity method is responsible for applying gravity to the player, making it fall to the ground"""
        
        self.fsm.update("fall", self)
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Check if player lands on the ground
        if self.rect.y >= 235:
            self.rect.y = 235
            self.is_on_ground = True
            self.velocity_y = 0