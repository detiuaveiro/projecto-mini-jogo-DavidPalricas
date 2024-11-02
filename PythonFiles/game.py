import pygame as pg
import game_map as gm
import player as pl
import sound_player as sp

def update_display(all_sprites, window, game_map,clock):
    """ Update the display for the game
        It clears the display, draws the map and the sprites , updates the display and sprites and sets the fps for the game (60)

        Parameters: all_sprites (stores the sprite group), window (stores the pygame display), game_map (stores the map), clock (stores the pygame clock)
    """
    window.fill((0, 0, 0))

    game_map.draw(window)

    all_sprites.update()
    all_sprites.draw(window)
       
    # Update the display
    pg.display.update()
         
    # 60 fps
    clock.tick(60)


def event_handler(running):
    """ Handle the events for the game
        It handles the events for the game like quitting the game
        
        Parameters: running (stores the state of the game)
        Return the running variable (stores the state of the game)
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    return running
    


def game_loop(all_sprites, window, clock, game_map):
    running = True
    background_music = sp.SoundPlayer("overworld_theme", True).play()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Update and draw all sprites
        all_sprites.update()
        window.fill((0, 0, 0))  # Clear the screen with black
        game_map.draw(window)   # Draw the game map
        all_sprites.draw(window)  # Draw all sprites on top of the map

        pg.display.flip()  # Update the display
        clock.tick(60)  # Cap the frame rate at 60 FPS

    pg.quit()



def setup_sprites():
    """ Set up the sprites for the game by creating a sprite group and adding the individual sprites to it
        Return the all_sprites variable (stores the sprite group)
    """
    all_sprites = pg.sprite.Group()
    grid_size = 40
    ground_level = 680  # Adjust this value based on your ground level
    player = pl.Player(grid_size, ground_level)
    all_sprites.add(player)
    return all_sprites


def setup_pygame():
    """ Set up the pygame environment 
        It initializes the pygame,sets up the displayand the clock

        Return the window variable ( stores the pygame display) and the clock variable (strores the pygame clock)
    """
    pg.init()

    # Set up the display
    window = pg.display.set_mode((1020, 720))
    pg.display.set_caption("Super Bowser")

    clock = pg.time.Clock()

    return window, clock


def main():
    window, clock = setup_pygame()
    window_width, window_height = 1020, 720
    all_sprites = setup_sprites()
    game_map = gm.Map(window_width, window_height)

    game_loop(all_sprites, window, clock, game_map)

if __name__ == "__main__":
    main()