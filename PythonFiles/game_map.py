import pygame as pg
import os

class Map:
    """ A class to represent the game map """

    def __init__(self, window_width, window_height):
        """Initialize the map, resize it to fit the window, and load map layout."""
        map_path = os.path.join(os.path.dirname(__file__), "../Assets/SpriteSheets/Map/overworld_map.bmp")
        self.map_image = pg.image.load(map_path)
        self.map_image = pg.transform.scale(self.map_image, (window_width, window_height))  # Resize map to window dimensions
        self.rect = self.map_image.get_rect()

        # Define map grid properties
        self.tile_size = 40  # Each tile is 40x40 pixels
        self.grid_width = window_width // self.tile_size
        self.grid_height = window_height // self.tile_size

        # Example layout: 1 = ground, 0 = empty space
        # This should ideally be loaded from a file for complex maps.
        self.layout = [
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            # More rows here based on map structure...
        ]

    def draw(self, window):
        """Draw the resized map and grid-based ground layout on the window."""
        window.blit(self.map_image, (0, 0))

    def is_ground(self, x, y):
        """Check if a given tile (x, y) represents ground."""
        tile_x = x // self.tile_size
        tile_y = y // self.tile_size

        # Ensure the coordinates are within the layout bounds
        if 0 <= tile_y < len(self.layout) and 0 <= tile_x < len(self.layout[0]):
            return self.layout[tile_y][tile_x] == 1
        return False

    def update_camera(self, player):
        """Update camera position based on player position."""
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery
