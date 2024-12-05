import pygame as pg
import os

class Map:
    def __init__(self, window_width, window_height, bitmap_relative_path="../Assets/SpriteSheets/Map/overworld_map_colored3.bmp"):
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

        self.floor = []
 
        self.question_marks = []

        self.blocks = []

        self.get_floor()

        with open("floor.txt", "w") as file:
            for floor in self.question_marks:
                file.write(f"{floor}\n")
    
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


    def get_floor(self):
        self.colors = []
        for y in range(self.window_height):
            for x in range(self.window_width):

                pixel = self.map_image.get_at((x,y))    
                if pixel[: 3] not in self.colors:
                    self.colors.append(pixel[: 3])

                self.test(pixel, (x, y))    

        with open("colors.txt", "w") as file:
            for color in self.colors:
                file.write(f"{color}\n")

    def test(self, pixel,coordinates):
        # Red Color
        FLOOR_COLOR = (255, 0, 0)

        QUESTION_MARK_COLOR = (163, 73, 164)

        BLOCK_COLOR = (63 , 72 , 204)
        
        # Ignore the alpha channel
        pixel_color = pixel[: 3]


        if pixel_color == FLOOR_COLOR:
            self.floor.append(pg.Rect(coordinates[0], coordinates[1], 1, 1))
        elif pixel_color == QUESTION_MARK_COLOR:
            self.question_marks.append(pg.Rect(coordinates[0], coordinates[1], 1, 1))
        elif pixel_color == BLOCK_COLOR:
            self.blocks.append(pg.Rect(coordinates[0], coordinates[1], 1, 1))

        

    
           
           
                


