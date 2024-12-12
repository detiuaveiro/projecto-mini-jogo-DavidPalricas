import pygame as pg
import game_map as gm
from player import Player
from kirby import Kirby
from observer import Observer
from camera import Camera
from consts import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_SECOND, GAME_TIME, TIMEOUT

# Define custom event types
PLAYER_DEATH_EVENT = pg.USEREVENT + 1
TIMEOUT_EVENT = pg.USEREVENT + 2
TIME_ALERT_EVENT = pg.USEREVENT + 3
JUMP_EVENT = pg.USEREVENT + 4
END_GAME_EVENT = pg.USEREVENT + 5
ENEMY_DEATH_EVENT = pg.USEREVENT + 6

def update_display(all_sprites, window, game_map, observer, game_time, camera):
    """
    The update_display function is responsible for updating the display of the game, drawing the game map, and updating the sprites.

    Args:
        - all_sprites: The group of all the sprites in the game.
        - window: The game window object.
        - game_map: The game map object.
        - score: The score object.
        - clock: The game clock object used for controlling the frame rate.
        - game_time: The time elapsed in the game.
    """
    
    observer.listener()
    # Clears the screen
    window.fill((107, 136, 255))  

    # Update camera to center on player
    game_map.draw(window, camera)

    player = next(sprite for sprite in all_sprites if isinstance(sprite, Player))

    # Draw the player with the camera offset
    window.blit(player.image, camera.apply(player))

    # Draw other sprites without the camera offset
    for sprite in all_sprites:
        if not isinstance(sprite, Player):
            window.blit(sprite.image, sprite.rect)

    observer.draw_ui_labels(window, game_time)
    
    # Updates the display
    pg.display.flip()

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
        elif event.type == PLAYER_DEATH_EVENT:
            print("Player has died")
            # Handle player death
        elif event.type == TIMEOUT_EVENT:
            print("Timeout occurred")
            # Handle timeout
        elif event.type == TIME_ALERT_EVENT:
            print("Time alert")
            # Handle time alert
        elif event.type == JUMP_EVENT:
            print("Player jumped")
            # Handle jump (play sound effect)
        elif event.type == END_GAME_EVENT:
            print("End of game")
            # Handle end of game
        elif event.type == ENEMY_DEATH_EVENT:
            print("Enemy has died")
            # Handle enemy death

    return running
   
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

    # Get the player object from all_sprites
    player = next(sprite for sprite in all_sprites if isinstance(sprite, Player)) 
    kirby = next(sprite for sprite in all_sprites if isinstance(sprite, Kirby))
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    enemies = [kirby]   
 
    observer = Observer(player, game_map, enemies)
    
    game_time = GAME_TIME * GAME_SECOND  # Total game time in milliseconds

    while running:
        running = event_handler(running)
        
        # Update player position
        all_sprites.update()
        
        camera.update(player)
        
        # Check if player has fallen off the map
        if player.rect.y > SCREEN_HEIGHT:
            pg.event.post(pg.event.Event(PLAYER_DEATH_EVENT))
            player.rect.x = 0
            player.rect.y = 235

        if len(enemies) > 0:
            for enemy in enemies:
                if enemy.dead:
                    pg.event.post(pg.event.Event(ENEMY_DEATH_EVENT))
                    observer.enemies = [enemies for enemies in observer.enemies if enemies.dead == False]
                    enemies.remove(enemy)
                    all_sprites.remove(enemy)

        # Decrease game time by the elapsed time in seconds
        elapsed_time = clock.tick(FPS) / 10000
        game_time -= elapsed_time

        # Draw everything
        update_display(all_sprites, window, game_map, observer, game_time, camera)

        if game_time <= 0:
            pg.event.post(pg.event.Event(TIMEOUT_EVENT))
            game_time = 0  # Ensure game_time does not go negative

        if int(game_time) % 10 == 0:
            pg.event.post(pg.event.Event(TIME_ALERT_EVENT))

    pg.quit()

def setup_sprites():
    """ The setup_sprites function creates the games sprites and adds it to the all_sprites group.
          
            Args:
                - game_map: The game map object.
    
            Returns:
                - all_sprites: The group of all the sprites in the game.
    """

    all_sprites = pg.sprite.Group()

    player = Player((0,235,25,31)) 
    all_sprites.add(player)

    kirby = Kirby((150, 252 , 18, 20))
    all_sprites.add(kirby)

    return all_sprites

def setup_pygame():
    """ The setup function for the pygame module, sets up the window and clock for the game.

        Returns:
            - window: The game window object.
            - clock: The game clock object used for controlling the frame rate.
    """
    pg.init()
    window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Super Bowser")
    clock = pg.time.Clock()

    return window, clock

def main():
    """ The main function of the game, sets up the pygame, creates the game map and sprites, and also runs the game loop.
    """
    window, clock = setup_pygame()

    game_map = gm.Map()
    #camera = game_map.get_camera()  # Commented out

    all_sprites = setup_sprites()  

    game_loop(all_sprites, window, clock, game_map)

if __name__ == "__main__":
    main()