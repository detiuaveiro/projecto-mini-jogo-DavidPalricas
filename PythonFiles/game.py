import pygame as pg
import finite_state_machine as fsm
from game_map import Map
from player import Player
from kirby import Kirby
from observer import Observer
from sound_player import SoundPlayer
from camera import Camera
from consts import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_SECOND, GAME_EVENTS
from game_ui import UI

class Game :
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls)
            cls._instance.__initialized = False

        return cls._instance
    
    def __init__(self) -> None:

        if not hasattr(self, 'initialized'):
            self.window, self.clock = self.setup_pygame()
            self.map = Map()
            self.fsm = fsm.FSM(self.set_states(), self.set_transitions())
            self.initialized = True

    def setup_pygame(self):
        pg.init()
        window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Super Bowser")
        clock = pg.time.Clock()

        return window, clock
    

    def set_states(self):
        self.playing = fsm.Playing()
        self.game_over = fsm.GameOver()

        return [self.playing, self.game_over]
    

    def set_transitions(self):
        return {
            "game_over": fsm.Transition(self.playing, self.game_over)
        }

def update_display(all_sprites, window, game_map, game_ui, camera):
    """
    The update_display function is responsible for updating the display of the game, drawing the game map, and updating the sprites.

    Args:
        - all_sprites: The group of all the sprites in the game.
        - window: The game window object.
        - game_map: The game map object.
        - game_ui: The game UI object.
        - game_time: The time elapsed in the game.
        - camera: The camera object used to center on the player.
    """
    
    # Clears the screen
    window.fill((107, 136, 255))  

    # Update camera to center on player
    game_map.draw(window, camera)

    # Draw all sprites with the camera offset
    for sprite in all_sprites:
        window.blit(sprite.image, camera.apply(sprite))

    game_ui.draw_labels(window)
    
    # Updates the display
    pg.display.flip()

def event_handler(running, audio_players, all_sprites):
    """ The event_handler function is responsible for handling the events in the game, such as quitting the game.
        
        Args:
            - running: A flag indicating whether the game is running or not.
            - all_sprites: The group of all the sprites in the game.
            - enemies: The list of enemy sprites.
            - observer: The observer object.

        Returns:
            - running: A flag indicating whether the game is running or not.

    """

    for event in pg.event.get():  
        if event.type == pg.QUIT :
            running = False

        elif event.type == GAME_EVENTS["QUIT_GAME_EVENT"]:
            print("Quit game event triggered")

            running = False

        elif event.type == GAME_EVENTS["PLAYER_DEATH_EVENT"]: 

            audio_players[1].play("bowser_death")
            player = next(sprite for sprite in all_sprites if isinstance(sprite, Player))
            player.respawn()

            game_ui = UI()
            game_ui.update_score(-50)

        elif event.type == GAME_EVENTS["TIMEOUT_EVENT"]:

            game = Game()
            game.fsm.update("game_over", game)

            # Stop the music player
            audio_players[0].stop()

            audio_players[1].play("game_over")
        elif event.type == GAME_EVENTS["TIME_ALERT_EVENT"]:
            # Play time warning sound effect
            game_ui = UI()
            game_ui.change_timer_text_color()

            audio_players[1].play("time_warning")

        elif event.type == GAME_EVENTS["PLAYER_JUMP_EVENT"]:
            audio_players[1].play("jump")

        elif event.type == GAME_EVENTS["END_GAME_EVENT"]:
            print("End of game")

        elif event.type == GAME_EVENTS["ENEMY_KILLED_EVENT"]:
            audio_players[1].play("enemy_killed")

            for sprite in all_sprites:
                if isinstance(sprite, Kirby) and sprite.dead: 
                    all_sprites.remove(sprite)
            
            game_ui = UI()
            game_ui.update_score(100)
  
    return running, all_sprites


def get_audio_players():
    """ The get_audio_players function is responsible for creating the audio player objects for the background music and sound effects.
        
        Returns:
            - audio_players: A list of audio player objects.
    """

    music_player = SoundPlayer(["overworld_theme", "game_over"], True)
    music_player.play("overworld_theme")

    sound_effecter = SoundPlayer(["jump","bowser_death","time_warning", "enemy_killed"], False)

    return [music_player, sound_effecter]
   
def game_loop(game):
    """ The game_loop function is responsible for running the game loop, updating the display, and handling events.
         It also checks if the player has fallen off the map and resets the player's position if needed.
         The function also plays the background music for the game and stops it when some event forces the game to stop.

         Args:
            - window: The game window object.
            - clock: The game clock object used for controlling the frame rate.
            - game_map: The game map object.
    """
    
    running = True


    window , clock , game_map = game.window, game.clock, game.map


    all_sprites = setup_sprites()  

    # Get the player object from all_sprites
    player = next(sprite for sprite in all_sprites if isinstance(sprite, Player)) 

    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    observer = Observer()

    audio_players = get_audio_players()

    delta_time = 0

    game_ui = UI()

    while running:

        if game.fsm.current == game.playing:
            running, all_sprites= event_handler(running, audio_players, all_sprites)
            
            # Update player position
            all_sprites.update()
            
            camera.update(player)

            delta_time += clock.tick(FPS)

            observer.observe(all_sprites)

            update_display(all_sprites, window, game_map, game_ui, camera)

            if delta_time >= GAME_SECOND:
                
                game_ui.update_timer()

                game_time = game_ui.time

                observer.observe_time_envents(game_time)

                delta_time -= GAME_SECOND

        elif game.fsm.current == game.game_over:

            all_sprites.empty()

            window.fill((0,0,0))

            pg.display.flip()

            pass

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


def main():
    """ The main function of the game, sets up the pygame, creates the game map and sprites, and also runs the game loop.
    """

    #camera = game_map.get_camera()  # Commented out

    game = Game()
    game_loop(game)

if __name__ == "__main__":
    main()



    
