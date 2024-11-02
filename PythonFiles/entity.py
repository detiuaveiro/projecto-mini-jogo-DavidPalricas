from sprite import Sprite
import pygame as pg

class Entity(Sprite):
    def __init__(self, sprite_path,grid_size, ground_level):

        super().__init__(sprite_path, (0, ground_level - grid_size, grid_size, grid_size))

        self.speed = None
        self.gravity = 0.5
        self.is_on_ground = True
        self.ground_level = ground_level
        self.grid_size = grid_size
        self.turned_right = True
        self.states = None
        self.transitions = None
        self.fsm = None
        self.name = None


    def set_states(self) :
        raise NotImplementedError
    

    def set_transitions(self):
        raise NotImplementedError
    

    def change_sprite(self,new_image):
        self.image = new_image
        
    


  