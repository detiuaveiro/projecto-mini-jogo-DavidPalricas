import pygame as pg
import game_map as gm
import player as pl
import sound_player as sp

def update_display(all_sprites, window, game_map, player, clock):
    """ Update the display: clear screen, draw map and sprites, update display and sprites, set FPS to 60. """
    window.fill((0, 0, 0))  # Clear screen

    # Update camera to center on player
    game_map.update_camera(player)
    game_map.draw(window)   # Draw the game map

    all_sprites.update()
    all_sprites.draw(window)

    pg.display.flip()  # Update display
    clock.tick(60)     # Cap FPS

def event_handler(running):
    """ Handle quitting events for the game. """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    return running

def game_loop(all_sprites, window, clock, game_map):
    running = True
    background_music = sp.SoundPlayer("overworld_theme", True).play()
    player = next(sprite for sprite in all_sprites if isinstance(sprite, pl.Player))  # Assuming the player is in all_sprites

    while running:
        running = event_handler(running)

        # Reset game if player falls off the map
        if player.rect.bottom > game_map.map_image.get_height():
            player.reset_position()
            print("Player fell off the map! Resetting position.")

        update_display(all_sprites, window, game_map, player, clock)

    pg.quit()

def setup_sprites(game_map):
    """ Set up the sprites for the game by creating a sprite group and adding the individual sprites to it
        Return the all_sprites variable (stores the sprite group)
    """
    all_sprites = pg.sprite.Group()
    grid_size = 40
    ground_level = 680
    player = pl.Player(grid_size, ground_level, game_map)  # Pass game_map to Player
    all_sprites.add(player)
    return all_sprites

def setup_pygame():
    """ Initialize pygame, set up display and clock. """
    pg.init()
    window = pg.display.set_mode((1020, 720))
    pg.display.set_caption("Super Bowser")
    clock = pg.time.Clock()
    return window, clock

def main():
    window, clock = setup_pygame()
    window_width, window_height = 1020, 720
    game_map = gm.Map(window_width, window_height)
    all_sprites = setup_sprites(game_map)  # Pass game_map to setup_sprites

    game_loop(all_sprites, window, clock, game_map)

if __name__ == "__main__":
    main()
