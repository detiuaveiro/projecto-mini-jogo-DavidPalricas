import pygame as pg
import os

class Map:
    """ The Map class is responsible for managing the game map in the game world

        The class has the following attributes:

            - tile_set (Surface): The tile set of the game map
            - FLOOR_TILE_WIDTH (int): The width of the floor tile
            - FLOOR_TILE_HEIGHT (int): The height of the floor tile
            - tile_per_row (int): The number of tiles per row
            - tile_per_col (int): The number of tiles per column
            - FLOOR_BLOCK (int): The index of the floor block
            - BRICK_BLOCK (int): The index of the brick block
            - QUESTION_BLOCK_USED (int): The index of the used question block
            - QUESTION_BLOCK (int): The index of the question block
            - map (list): The game map
            - floor_blocks (list): The list of floor blocks
            - brick_blocks (list): The list of brick blocks
            - question_blocks (list): The list of question blocks
    """
    def __init__(self) -> None:
        """ Initializes a new instance of the Map class and sets up the game map atrributes"""

        tile_set_path = (os.path.join(os.path.dirname(__file__), "../Assets/SpriteSheets/Map/overworld_tileset.png"))
        self.tile_set = pg.image.load(tile_set_path)

        self.FLOOR_TILE_WIDTH = 16
        self.FLOOR_TILE_HEIGHT = 19

        self.tile_per_row = self.tile_set.get_width() // self.FLOOR_TILE_WIDTH
        self.tile_per_col = self.tile_set.get_height() // self.FLOOR_TILE_HEIGHT

        self.FLOOR_BLOCK = 0
        self.BRICK_BLOCK = 1
        self.QUESTION_BLOCK_USED = 2
        self.QUESTION_BLOCK = 3

        self.map = [[],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [None] * 22 + [self.BRICK_BLOCK] * 3 + [None],
                    [None] * 5  + [self.BRICK_BLOCK,self.QUESTION_BLOCK,self.BRICK_BLOCK] ,
                    [None] * 17 + [self.BRICK_BLOCK]*2 + [self.QUESTION_BLOCK,self.BRICK_BLOCK],
                    [],
                    [],
                    [self.FLOOR_BLOCK] * 31,
        ]

        self.floor_blocks = []
        self.brick_blocks = []
        self.question_blocks = []

    
    def draw(self,window):
        """ The draw method is responsible for drawing the game map on the screen  
                Args:
                    - window (Surface): The game window object
        """
        for row_index,row in enumerate(self.map):
            for col_index, tile_index in enumerate(row):
                if tile_index is None:
                    continue
                tile_image = self.get_tile_image(self.tile_set,tile_index,(col_index,row_index))
                window.blit(tile_image,(col_index * self.FLOOR_TILE_WIDTH, row_index * self.FLOOR_TILE_HEIGHT))

    def get_tile_image(self,tile_set,tile_index, map_index):
        """ The get_tile_image method is responsible for getting the tile image from the tile set and setting up the blocks colliders
             
             Args:
                 - tile_set (Surface): The tile set of the game map
                 - tile_index (int): The index of the tile in the tile set
                 - map_index (tuple): The index of the tile in the game map
             
             Returns:
                 - Surface: The tile image from the tile set
        """
        row, column = tile_index // self.tile_per_row, tile_index % self.tile_per_row
        block_width, block_height = (self.FLOOR_TILE_WIDTH, self.FLOOR_TILE_HEIGHT) if tile_index == self.FLOOR_BLOCK else (17, 19)
       
        x, y = column * block_width, row * block_height
                  
        block_collider = pg.Rect(map_index[0] * self.FLOOR_TILE_WIDTH ,map_index[1] * self.FLOOR_TILE_HEIGHT, block_width, block_height)
          
        if tile_index == self.BRICK_BLOCK:
            self.brick_blocks.append((block_collider,map_index))
        elif tile_index == self.QUESTION_BLOCK:
            self.question_blocks.append((block_collider, map_index))
        else:
            self.floor_blocks.append((block_collider, map_index))

        return tile_set.subsurface((x, y, self.FLOOR_TILE_WIDTH, self.FLOOR_TILE_HEIGHT)) 
