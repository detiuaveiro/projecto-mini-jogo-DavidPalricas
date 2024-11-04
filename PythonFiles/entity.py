from sprite import Sprite
from animator import Animator

class Entity(Sprite):
    """The Entity class is responsible for managing the entities in the game world

       The class has the following attributes:
          - speed: The speed of the entity
          - gravity: The gravity acting on the entity
          - is_on_ground: A flag indicating whether the entity is on the ground
          - ground_level: The level of the ground in the game world
          - grid_size: The size of the grid in the game world
          - turned_right: A flag indicating whether the entity is turned right
          - states: The states of the entity, e.g. idle, walk, jump
          - transitions: The transitions between the entity's states
          - fsm: The finite state machine of the entity
          - name: The name of the entity
          - animator: The animator of the entity
    """
    def __init__(self, sprite_path,grid_size, ground_level)-> None:
        """ 
            Initializes a new instance of the Entity class, and calls the constructor of the Sprite class (the parent class) 
            
            Args:
                - sprite_path (str): The path to the sprite image file
                - grid_size (int): The size of the grid in the game world
                - ground_level (int): The level of the ground in the game world
        """

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
        self.animator = Animator()

    def set_states(self) :
        """
            The set_states method is responsible for setting the states of the entity
            The method should be overridden by the derived classes
        """

        raise NotImplementedError
    

    def set_transitions(self):
        """
            The set_transitions method is responsible for setting the transitions between the entity's states
            The method should be overridden by the derived classes
        """
        
        raise NotImplementedError
    

  