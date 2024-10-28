import pygame as pg
import os

class Map:
    def __init__(self, window_width, window_height):
        # Construct the absolute path to the sprite image
        sprite_path = os.path.join(os.path.dirname(__file__), "../Assets/SpriteSheets/Map/overworld_map.bmp")
        if not os.path.isfile(sprite_path):
            raise FileNotFoundError(f"No such file: '{sprite_path}'")
        self.tile_set = pg.image.load(sprite_path).convert_alpha()
        self.TILE_WIDTH = 17
        self.TILE_HEIGHT = 19
        self.tile_per_row = self.tile_set.get_width() // self.TILE_WIDTH
        self.tile_per_col = self.tile_set.get_height() // self.TILE_HEIGHT

        # Calculate the scale factor to fill the window
        self.scale_factor_x = window_width / (self.tile_per_row * self.TILE_WIDTH)
        self.scale_factor_y = window_height / (self.tile_per_col * self.TILE_HEIGHT)

        # Calculate the number of rows and columns needed to fill the screen
        num_cols = int(window_width // (self.TILE_WIDTH * self.scale_factor_x))
        num_rows = int(window_height // (self.TILE_HEIGHT * self.scale_factor_y))

        # Generate the map dynamically
        self.map = [[(row * num_cols + col) % (self.tile_per_row * self.tile_per_col) for col in range(num_cols)] for row in range(num_rows)]
    
    def draw(self, window):
        for row_index, row in enumerate(self.map):
            for col_index, tile_index in enumerate(row):
                tile_image = self.get_tile_image(self.tile_set, tile_index)
                scaled_tile_image = pg.transform.scale(tile_image, (int(self.TILE_WIDTH * self.scale_factor_x), int(self.TILE_HEIGHT * self.scale_factor_y)))
                window.blit(scaled_tile_image, (col_index * self.TILE_WIDTH * self.scale_factor_x, row_index * self.TILE_HEIGHT * self.scale_factor_y))

    def get_tile_image(self, tile_set, tile_index):
        row = tile_index // self.tile_per_row
        column = tile_index % self.tile_per_row

        x = column * self.TILE_WIDTH 
        y = row * self.TILE_HEIGHT 

        return tile_set.subsurface((x, y, self.TILE_WIDTH, self.TILE_HEIGHT))