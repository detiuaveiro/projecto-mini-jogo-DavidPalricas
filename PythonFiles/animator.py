import pygame as pg
import os
class Animator:
    def __init__(self) -> None:
        self.current_animation = "idle"
        self.animation_index = 0
        self.animation_delay = 100
        self.animations_frames = None
        self.last_update = 0
               
    def play_animation(self,state,entity):
     # Check if the current animation is different from the new animation
     if self.current_animation != state:
        self.current_animation = state
        self.animation_index = 0  # Reset the animation
        self.last_update = 0
        self.animations_frames = self.load_animation_frames(entity, state)
     
     # Get the current time in milliseconds since Pygame was initialized
     now = pg.time.get_ticks()
    
    # Check if the time elapsed since the last update is greater than the animation delay
     if now - self.last_update > self.animation_delay:
        # Update the last update time to the current time
        self.last_update = now
        
        # Increment the animation index and wrap it around using modulo to stay within the valid range
        self.animation_index = (self.animation_index + 1) % len(self.animations_frames)
        
        entity.image = self.animations_frames[self.animation_index]

        if not entity.turned_right:
            entity.image = pg.transform.flip(entity.image, True, False)
    
    def load_animation_frames(self, entity, state):
        """ Load the animation frames for the given state """

        new_image = pg.image.load(os.path.join(os.path.dirname(__file__), f"../Assets/SpriteSheets/{entity.name}/{state}/{entity.name}_{state}.png")).convert_alpha()
        
        # Check if the image is a tileset (based on the width of the original sprite)
        if new_image.get_width() > entity.dimensions[0]:
            return self.split_tileset(new_image, entity.dimensions)
        else:      
            # To ensure that all the frames have the same width as the original sprite
            return [pg.transform.scale(new_image,(entity.dimensions[0],new_image.get_height()))]

    def split_tileset(self, tile_set, sprite_dimensions):
        """ Split the tileset into individual frames """
        frames = []
        
        sprite_width, sprite_height = sprite_dimensions

        num_frames = round(tile_set.get_width() / sprite_width)
        
        for i in range(num_frames):
            if i == 0:
                frame = tile_set.subsurface((i * sprite_width, 0, sprite_width, tile_set.get_height()))
            else:
                frame = tile_set.subsurface((i * sprite_width, 0, tile_set.get_width() - i * sprite_width, tile_set.get_height()))
       
            # To Ensure that all the frames have the same dimensions, scale the frame to the sprite original width
            frame = pg.transform.scale(frame, (sprite_width, tile_set.get_height()))

            frames.append(frame)

        return frames
