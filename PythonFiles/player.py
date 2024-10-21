import pygame as pg
import sprite as sp

class Player(sp.Sprite):
    def __init__(self): 
        super().__init__("../Assets/SpriteSheets/Bowser/Idle/bowser_idle.png",(0,350,80,40))
        
        self.movement_keys = [pg.K_a, pg.K_d, pg.K_RIGHT, pg.K_LEFT, pg.K_SPACE]

        self.speed = 10
        self.gravity = 0.5
        self.jump_speed = 50
        self.player_turned_right = True
        self.is_on_ground = True

    def move(self,key):
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
        if (self.is_on_ground):
            self.is_on_ground = False
            self.rect.y -= self.jump_speed


    def handling_fall(self):
        if not self.is_on_ground:
            self.rect.y += self.gravity

            if self.rect.y >= 350:
                self.is_on_ground = True