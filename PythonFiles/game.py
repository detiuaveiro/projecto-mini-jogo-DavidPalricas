import pygame as pg
import game_map as gm
from player import Player
import sound_player as sp
from kirby import Kirby
from block import Block

def update_display(all_sprites, window, game_map, player, clock):
    """
    The update_display function is responsible for updating the display of the game, drawing the game map, and updating the sprites.

    Args:
        - all_sprites: The group of all the sprites in the game.
        - window: The game window object.
        - game_map: The game map object.
        - player: The player object.
        - clock: The game clock object used for controlling the frame rate.
    """
    # Clears the screen
    window.fill((0, 0, 0))  

    # Update camera to center on player
    game_map.update_camera(player)

    # Draw the game map with camera
    game_map.draw(window)   

    # Update all sprites and draw them on top of the map
    all_sprites.update()
    all_sprites.draw(window)
    
    # Updates the display
    pg.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)

def event_handler(running):
    """ The event_handler function is responsible for handling the events in the game, such as quitting the game.
        
        Args:
            - running: A flag indicating whether the game is running or not.

        Returns:
            - running: A flag indicating whether the game is running or not.

    """

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
    return running


def check_collision(player, game_map):
    """ The check_collision function checks if the player has collided with any of the blocks in the game map.

        Args:
            - player: The player object.
            - game_map: The game map object.

        Returns:
            - pixel_index: The index of the block that the player has collided with.
    """

    if player.rect.collidelist(game_map.question_marks) != -1 or player.rect.collidelist(game_map.blocks) != -1:
            
        is_question_block = player.rect.collidelist(game_map.question_marks) != -1

        pixel_index = player.rect.collidelist(game_map.question_marks) if is_question_block else player.rect.collidelist(game_map.blocks)

        pixel_block = game_map.question_marks[pixel_index] if is_question_block else game_map.blocks[pixel_index]

        block = Block(pixel_block, game_map, is_question_block)
            
        if block.is_question_block:
            block.block_hitted()


def game_loop(all_sprites, window, clock, game_map):
    """ The game_loop function is responsible for running the game loop, updating the display, and handling events.
         It also checks if the player has fallen off the map and resets the player's position if needed.
         The function also plays the background music for the game and stops it when some event forces the game to stop.

         Args:
            - all_sprites: The group of all the sprites in the game.
            - window: The game window object.
            - clock: The game clock object used for controlling the frame rate.
            - game_map: The game map object.
    """

    running = True

    # The background_music variable is unused for now, but it will be used in the future.
    background_music = sp.SoundPlayer("overworld_theme", True).play()

    # Get the player object from all_sprites
    player = next(sprite for sprite in all_sprites if isinstance(sprite, Player))  
 
    
    while running:
        running = event_handler(running)

        check_collision(player, game_map)

        # Reset game if player falls off the map
        if player.rect.bottom > game_map.map_image.get_height():
            player.reset_position()
            print("Player fell off the map! Resetting position.")

        # Update camera to follow player
        game_map.update_camera(player)

        # Draw everything
        update_display(all_sprites, window, game_map, player, clock)

    pg.quit()



def setup_sprites(game_map):
    """ The setup_sprites function creates the games sprites and adds it to the all_sprites group.
          
            Args:
                - game_map: The game map object.
    
            Returns:
                - all_sprites: The group of all the sprites in the game.
    """

    all_sprites = pg.sprite.Group()
    grid_size = 32
    ground_level = game_map.map_image.get_height() - grid_size
    player = Player(grid_size, ground_level, game_map) 
    kirby = Kirby(grid_size, ground_level)
    all_sprites.add(player)
    all_sprites.add(kirby)

    return all_sprites

def setup_pygame():
    """ The setup function for the pygame module, sets up the window and clock for the game.

        Returns:
            - window: The game window object.
            - clock: The game clock object used for controlling the frame rate.
    """
    pg.init()
    window = pg.display.set_mode((800, 277))
    pg.display.set_caption("Super Bowser")
    clock = pg.time.Clock()

    return window, clock

def main():
    """ The main fyunction of the game, sets up the pygame, creates the game map and sprites, and also runs the game loop.
    """
    window, clock = setup_pygame()

    window_width, window_height = window.get_size()
    game_map = gm.Map(window_width, window_height)
    camera = game_map.get_camera()

    all_sprites = setup_sprites(game_map)  

    game_loop(all_sprites, window, clock, game_map)

if __name__ == "__main__":
    main()
