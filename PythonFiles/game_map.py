import pygame as pg
import os

class Map:
    def __init__(self, window_width, window_height, bitmap_relative_path="../Assets/SpriteSheets/Map/overworld_map.bmp"):
        """
        Initializes the Map object, including loading the bitmap and setting up the camera.
        
        :param window_width: Width of the game window.
        :param window_height: Height of the game window.
        :param bitmap_relative_path: Relative path to the bitmap image file.
        """
        self.window_width = window_width
        self.window_height = window_height

        # Construct the absolute path to the bitmap file
        self.bitmap_path = os.path.join(os.path.dirname(__file__), bitmap_relative_path)
        
        # Load the bitmap image as the map background
        self.map_image = pg.image.load(self.bitmap_path)
        self.map_rect = self.map_image.get_rect()
        self.camera = self.map_rect.clip(pg.Rect(0, 0, window_width, window_height))
        
    def get_camera(self):
        """
        Returns the camera object.
        
        :return: The camera object.
        """
        return self.camera
    
    def get_map_rect(self):
        """
        Returns the map rectangle.
        
        :return: The map rectangle.
        """
        self.map_rect = pg.transform.scale(self.map_image, (self.window_width, self.window_height)).get_rect()
        return self.map_rect

    def update_camera(self, player):
        """
        Updates the camera to follow the player.
        
        :param player: The player object.
        """
        # Set the camera center to the player's position
        self.camera.center = player.rect.x, self.window_height / 2 
        
        # Clamp the camera to the bounds of the map
        # Ensure that the camera doesn't show empty areas beyond the map
        self.camera.clamp_ip(self.map_rect)

        # Optional: If the map is smaller than the screen, center the camera
        if self.map_rect.width < self.window_width:
            self.camera.centerx = self.map_rect.centerx
        if self.map_rect.height < self.window_height:
            self.camera.centery = self.map_rect.centery

    def draw(self, window):
        """
        Draws the visible part of the map to the window.
        
        :param window: The game window surface.
        """
        # Blit the map image relative to the camera (this ensures the camera follows the player)
        window.blit(self.map_image, (0, 0), self.camera)