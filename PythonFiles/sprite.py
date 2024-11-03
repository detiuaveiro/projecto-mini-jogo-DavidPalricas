import pygame as pg
import pygame.sprite as pgs
class Sprite:
    """ A class to represent a sprite in the game"""

    def __init__(self,sprite_path,coordinates): 
        """ Constructor for the Sprite class
            Set the image ,the rect attributes and the add_internal and remove_internal methods
            
            Parameters: sprite_path (stores the path to the sprite image), coordinates (stores the coordinates of the sprite)
        """    

        self.image = pg.image.load(sprite_path).convert_alpha()
        self.dimensions = (self.image.get_width(), self.image.get_height())
        self.rect = pgs.Rect(coordinates)
        
        # The add_internal and remove_internal methods are implemented to be possible for add and remove instance of the Sprite class from the sprite group define in the game.py
        self.add_internal = pgs.Group.add
        self.remove_internal = pgs.Group.remove
    
    def update(self):
        """ Method to update the sprite
            This method must be implemented even if it does nothing, for  instance of the Sprite class could be updated by  the sprite group define in the game.py
        """
        pass  
 