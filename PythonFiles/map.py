import pygame as pg

class Map:
    def __init__(self):
        self.tile_set = pg.image.load("../Assets/SpriteSheets/Map/overworld_tileset.png")
        self.TILE_WIDTH = 17
        self.TILE_HEIGHT = 19
        self.tile_per_row = self.tile_set.get_width() // self.TILE_WIDTH
        self.tile_per_col = self.tile_set.get_height() // self.TILE_HEIGHT

        self.map = [[],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [0,0,0,0],
        ]
    
    def draw(self,window):
        for row_index,row in enumerate(self.map):
            for col_index, tile_index in enumerate(row):
                tile_image = self.get_tile_image(self.tile_set,tile_index)
                window.blit(tile_image,(col_index * self.TILE_WIDTH, row_index * self.TILE_HEIGHT))

    def get_tile_image(self,tile_set,tile_index):
        row = tile_index // self.tile_per_row
        column = tile_index % self.tile_per_row

        x = column * self.TILE_WIDTH 
        y = row * self.TILE_HEIGHT 

        return tile_set.subsurface((x,y,self.TILE_WIDTH,self.TILE_HEIGHT))

        