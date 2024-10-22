import pygame as pg
import pygame.sprite as pgs
import map as mp
import player as pl

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


def event_handler(running, player):
    """ Handle the events for the game
        It handles the events for the game like quitting the game and moving the player

        Parameters: running (stores the state of the game), player (stores the player sprite)
        Return the running variable (stores the state of the game)
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            player.move(event.key)

    return running
    


def game_loop(all_sprites, window, clock):
    """ Game loop for the game
        It runs the game loop, handles events, do the game logic and updates the display
        If running is False, the game loop stops

        Parameters: all_sprites (stores the sprite group), window (stores the pygame display), clock (stores the pygame clock)
    """
    game_map = mp.Map()
    player  = all_sprites.sprites()[0]
    running = True

    # Set up the game loop
    while running:
        running = event_handler(running, player)

        player.handling_fall()
     
        update_display(all_sprites, window, game_map,clock)



def setup_sprites(window):
    """ Set up the sprites for the game by creating a sprite group and adding the individual srites to it
        Return the all_sprites variable ( stores the sprite group)

        Parameters: window (stores the pygame display)
    """
    all_sprites = pgs.Group()

    player = pl.Player()

    all_sprites.add(player)

    all_sprites.draw(window)

    return all_sprites


def setup_pygame():
    """ Set up the pygame environment 
        It initializes the pygame,sets up the displayand the clock

        Return the window variable ( stores the pygame display) and the clock variable (strores the pygame clock)
    """
    pg.init()

    # Set up the display
    window = pg.display.set_mode((600, 400))
    pg.display.set_caption("Super Bowser")

    clock = pg.time.Clock()

    return window, clock


def main():
    """ Main function for the game 
        It sets up the game and runs the game loop
    """
 
    window,clock =  setup_pygame()

    all_sprites = setup_sprites(window)

    game_loop(all_sprites, window, clock)
   
    pg.quit()

if __name__ == "__main__":
    main()