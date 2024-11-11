from entity import Entity
import finite_state_machine as fsm
import pygame as pg
import os

class Kirby(Entity):
    
    def __init__(self, grid_size, ground_level): 
        """
            Initializes a new instance of the Kirby class, and calls the constructor of the Entity class (the parent
       """
        
        sprite_path = os.path.join(os.path.dirname(__file__), "../Assets/SpriteSheets/Enemies/Kirby/Idle/Kirby_idle.png")
        
        super().__init__(sprite_path, grid_size, ground_level)


        # Set up the kirby's attributes
        self.walked_distance = 0
           
        # Set up the atrributes inherited from the Entity class
        self.speed = 1.2
        self.turned_right = True
        self.name = "Kirby"

        
         # Initialize FSM and states
        self.fsm = fsm.FSM(self.set_states(), self.set_transitions())


    def set_states(self):
        """ The set_states method is responsible for setting the states of the kirby e.g. (idle, walk, jump)
            Returns:
                - states (list): A list of the kirby's states
         """
        self.idle = fsm.Idle()
        self.walk = fsm.Walk()

        return [self.idle, self.walk]
    
    def set_transitions(self):
        """ The set_transitions method is responsible for setting the transitions between the kirby's states
            Returns:
                - transitions (list): A list of the kirby's transitions
        """
        return {
            "walk": fsm.Transition(self.idle, self.walk,),
            "idle": fsm.Transition(self.walk, self.idle)
        }
    
    def update(self):
        """ The update method is responsible for updating the kirby's FSM
        """
        self.patrol()

        self.animator.play_animation(self.fsm.current.name, self)


    def patrol(self):
        if self.turned_right:

            if self.fsm.current == self.idle:
                self.fsm.update("walk", self)

            self.walked_distance += self.speed
            self.rect.x += self.speed 
        else:

            if self.fsm.current == self.idle:
                self.fsm.update("walk", self)

            self.walked_distance += self.speed
            self.rect.x -= self.speed

        if self.walked_distance >= 100:
            self.turned_right =  not self.turned_right
            self.walked_distance = 0

            if not self.turned_right:
                self.image = pg.transform.flip(self.image, True, False)
            else:
                self.image = pg.transform.flip(self.image, False, False)
                
            self.fsm.update("idle", self)
        

        
     