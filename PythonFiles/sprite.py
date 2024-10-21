import pygame as pg
import pygame.sprite as pgs
class Sprite:
    def __init__(self,sprite_path,coordinates):      
         self.image = pg.image.load(sprite_path).convert_alpha()
         self.rect = pgs.Rect(coordinates)

         self.add_internal = pgs.Group.add
         self.remove_internal = pgs.Group.remove
    
    # This method must be implemented
    # To add the sprite to the group
    def update(self):
        pass


        