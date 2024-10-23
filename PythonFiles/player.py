import pygame as pg
import sprite as s
import sound_player as sp

class Player(s.Sprite):
    """ A class to represent the player in the game
        The player class inherits from the Sprite class
    """
    def __init__(self): 
        """ Constructor for the Player class
            It calls the constructor of the parent class and initializes the player attributes
            Set the player speed, gravity, jump speed, player_turned_right , is_on_ground and sound_player attributes
        """

        """ The super() function is used to call the constructor (__init__()) of the parent class."""
        super().__init__("../Assets/SpriteSheets/Bowser/Idle/bowser_idle.png",(0,350,80,40))
        
        self.movement_keys = [pg.K_a, pg.K_d, pg.K_RIGHT, pg.K_LEFT, pg.K_SPACE]

        self.speed = 1.8
        self.gravity = 0.5
        self.jump_speed = 50
        self.player_turned_right = True
        self.is_on_ground = True

        self.sound_player = sp.SoundPlayer("jump",False)
    
    def move(self,keys):
        """ Method to move the player
            If the player is not on the ground, it calls the handling_fall method
            Othwerise it moves the player based in the key pressed, to the right or to the left and makes the player jump by calling the jump method
            It also flips the player image based on the direction the player is moving and if the LSHIFT key is pressed the player moves faster
            
            Parameters: key (stores the key pressed by the player)
        """

        if not self.is_on_ground:
            self.handling_fall()

        else: 
            if (keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]):
                    self.jump()
            elif (keys[pg.K_d] or keys[pg.K_RIGHT]):
                    self.rect.x += 2 * self.speed if keys[pg.K_LSHIFT] else self.speed

                    if not self.player_turned_right:
                            self.image = pg.transform.flip(self.image,True,False)
                            self.player_turned_right = True

            elif (keys[pg.K_a] or keys[pg.K_LEFT]):
                        self.rect.x -=  2 * self.speed if keys[pg.K_LSHIFT] else self.speed
                        
                        if self.player_turned_right:
                            self.image = pg.transform.flip(self.image,True,False)
                            self.player_turned_right = False
    
    def jump(self):
        """ Method to make the player jump
            It makes the player jump if the and plays the jump sound sound effect
            It also sets the is_on_ground attribute to False
        """
      
        self.sound_player.play()
        self.is_on_ground = False
        self.rect.y -= self.jump_speed

    def handling_fall(self):
        """ Method to handle the player falling
            It makes the player fall if the player is not on the ground
            When the players reach the ground, it sets the is_on_ground attribute to True
        """
        if not self.is_on_ground:
            self.rect.y += self.gravity

            if self.rect.y >= 350:
                self.is_on_ground = True