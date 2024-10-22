import pygame as pg
import sprite as sp

class Player(sp.Sprite):
    """ A class to represent the player in the game
        The player class inherits from the Sprite class
    """
    def __init__(self): 
        """ Constructor for the Player class
            It calls the constructor of the parent class and initializes the player attributes
            Set the player speed, gravity, jump speed, player_turned_right and is_on_ground attributes
        """

        """ The super() function is used to call the constructor (__init__()) of the parent class."""
        super().__init__("../Assets/SpriteSheets/Bowser/Idle/bowser_idle.png",(0,350,80,40))
        
        self.movement_keys = [pg.K_a, pg.K_d, pg.K_RIGHT, pg.K_LEFT, pg.K_SPACE]

        self.speed = 10
        self.gravity = 0.5
        self.jump_speed = 50
        self.player_turned_right = True
        self.is_on_ground = True
    
    def move(self,key):
        """ Method to move the player
            It moves the player based in the key pressed, to the right or to the left and makes the player jump by calling the jump method
            
            Parameters: key (stores the key pressed by the player)
        """
        if key in self.movement_keys:
            if (key == pg.K_SPACE):
                self.jump()
            elif (key == pg.K_d or key == pg.K_RIGHT):
                self.rect.x += self.speed

                if not self.player_turned_right:
                    self.image = pg.transform.flip(self.image,True,False)
                    self.player_turned_right = True

            elif (key == pg.K_a or key == pg.K_LEFT):
                    self.rect.x -= self.speed
                    
                    if self.player_turned_right:
                        self.image = pg.transform.flip(self.image,True,False)
                        self.player_turned_right = False
   
    def jump(self):
        """ Method to make the player jump
            It makes the player jump if the player is on the ground
        """
        if (self.is_on_ground):
            self.is_on_ground = False
            self.rect.y -= self.jump_speed

    def handling_fall(self):
        """ Method to handle the player falling
            It makes the player fall if the player is not on the ground
        """
        if not self.is_on_ground:
            self.rect.y += self.gravity

            if self.rect.y >= 350:
                self.is_on_ground = True