import pygame as pg
from entity import Entity
import sound_player as sp
import finite_state_machine as fsm
import os

class Player(Entity):
    """
        The Player class is responsible for managing the player entity in the game world
       
        The class has the following attributes:
            - jump_speed: The speed of the player's jump
            - sound_player: The sound player of the player
            - last_key_pressed: The last key pressed by the player
            - game_map: The game map
    """

    def __init__(self, grid_size, ground_level, game_map): 
        """
            Initializes a new instance of the Player class, and calls the constructor of the Entity class (the parent class)
            Loads the sprite image for the player
            Sets up the player's attributes and the attributes inherited from the Entity class including the FSM and its states

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

        self.animator.play_animation(self.fsm.current.name, self)


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
            self.sound_player.play()
            self.is_on_ground = False
            self.velocity_y = -self.jump_speed
     
    def apply_gravity(self):
        """ The apply_gravity method is responsible for applying gravity to the player, making it fall to the ground"""
 
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Check if player lands on the ground
        if self.rect.bottom >= self.ground_level:
            self.rect.bottom = self.ground_level
            self.is_on_ground = True
            self.velocity_y = 0
            self.fsm.update("fall", self)

    def break_block(self,removed_pixel, is_question_mark = True):     
        pixel_line = []
        
        self.game_map.question_marks.remove(removed_pixel)

        for pixel_block in self.game_map.question_marks:
            if removed_pixel.y == pixel_block.y:
                pixel_line.append(pixel_block)
                self.game_map.question_marks.remove(pixel_block)
                self.game_map.map_image.set_at((pixel_block.x, pixel_block.y), (0, 162, 232)) 
        
        if len(pixel_line) == 0:
            return
        
        area_width = len(pixel_line) + 1
    
        pixel_line.sort(key=lambda pixel: pixel.x)

        median_point = ((pixel_line[0].x + pixel_line[-1].x) // 2 , pixel_line[0].y)
       
        block_center = None

        for floor in self.game_map.floor:
            if floor.x == median_point[0] and floor.y < median_point[1]:
                self.game_map.floor.remove(floor)

                block_center = floor.x , (floor.y + median_point[1]) // 2

                break

        if block_center:

            area_width = 17
            area_height = 17
            block_center_x = block_center[0]
            block_center_y = block_center[1]

                # Definir os limites da área
            x_min = round(block_center_x - area_width / 2)
            x_max = round(block_center_x + area_width / 2)
            y_min = round(block_center_y - area_height / 2)
            y_max = round(block_center_y + area_height / 2)

            print(x_min, x_max, y_min, y_max)

            for y in range(y_min, y_max):
                for x in range(x_min, x_max):
                    # Switches the pixels colors of the block for the sky color
                    self.game_map.map_image.set_at((x, y), (0, 162, 232))  
                    
                    # Remover blocos das listas usando coordenadas
                    self.game_map.question_marks[:] = [block for block in self.game_map.question_marks if not (block.x == x and block.y == y)]
                    self.game_map.floor[:] = [floor for floor in self.game_map.floor if not (floor.x == x and floor.y == y)]
                 