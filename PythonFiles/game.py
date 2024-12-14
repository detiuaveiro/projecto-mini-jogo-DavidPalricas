import pygame as pg
import finite_state_machine as fsm
from game_map import Map
from player import Player
from kirby import Kirby
from observer import Observer
from sound_player import SoundPlayer
from camera import Camera
from consts import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_SECOND, GAME_EVENTS, FONT_PATH, FONT_SIZE, COLORS
from game_ui import UI
import os

class Game:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls)
            cls._instance.__initialized = False

        return cls._instance
    
    def __init__(self) -> None:
        if not self.__initialized:
            self.window, self.clock = self.setup_pygame()
            self.map = None
            self.fsm = fsm.FSM(self.set_states(), self.set_transitions())
            self.__initialized = True
            self.player = None
            self.ui = None
            self.audio_players = None
            self.camera = None
            self.delta_time = 0
            self.all_sprites = None

    def setup_pygame(self):
        """
        Initializes pygame and sets up the game window and clock.
        """
        pg.init()
        window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Super Bowser")
        clock = pg.time.Clock()

        return window, clock
    
    def set_states(self):
        """
        Creates and associates the multiple states the game has.
        """
        self.start_menu = fsm.StartMenu()
        self.playing = fsm.Playing()
        self.game_over = fsm.GameOver()

        return [self.start_menu, self.playing, self.game_over]
    
    def set_transitions(self):
        """
        Manages the transitions based on the states created before.
        """
        return {
            "start_game": fsm.Transition(self.start_menu, self.playing),
            "game_over": fsm.Transition(self.playing, self.game_over),
            "restart_game": fsm.Transition(self.game_over, self.playing)
        }

    def reset_game(self):
        """
        Resets the game by initializing the map and updating the FSM to the start game state.
        """
        self.map = Map()
        self.fsm.update("start_game", self)
   
    def play_level(self):    
        """
        Updates all sprites, the camera, and handles game events and UI updates.
        """
        self.all_sprites.update()
        self.camera.update(self.player)
        self.delta_time += self.clock.tick(FPS)
        self.observer.observe(self.all_sprites)
     
        if self.delta_time >= GAME_SECOND:
            self.ui.update_timer()
            game_time = self.ui.time
            self.observer.observe_time_envents(game_time)
            self.delta_time -= GAME_SECOND

    def setup_sprites(self):
        """
        Sets up the game sprites, including the player and multiple Kirby instances.
        """
        all_sprites = pg.sprite.Group()
    
        player = Player((0, 235, 25, 31))
        all_sprites.add(player)
    
        original_kirby = Kirby((150, 252, 18, 20))
        all_sprites.add(original_kirby)
    
        kirby2 = original_kirby.clone()
        kirby2.rect.topleft = (350, 252)
        all_sprites.add(kirby2)
    
        kirby3 = original_kirby.clone()
        kirby3.rect.topleft = (570, 195)
        all_sprites.add(kirby3)
    
        kirby4 = original_kirby.clone()
        kirby4.rect.topleft = (770, 138)
        all_sprites.add(kirby4)
    
        kirby5 = original_kirby.clone()
        kirby5.rect.topleft = (1000, 195)
        all_sprites.add(kirby5)
    
        return all_sprites
    
    def setup_game_level(self):
        """
        Sets up the game level by initializing the map, sprites, player, camera, observer, audio players, and UI.
        """
        self.map = Map()
        self.all_sprites = self.setup_sprites()  
        self.player = next(sprite for sprite in self.all_sprites if isinstance(sprite, Player)) 
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.observer = Observer()
        self.audio_players = get_audio_players()
        self.delta_time = 0
        self.ui = UI()
 
    def display_start_menu(self):
        """
        Displays the start menu screen with the game title and instructions.
        """
        self.window.fill(COLORS["BLACK"])
        font_path = os.path.join(os.path.dirname(__file__), FONT_PATH)
        font = pg.font.Font(font_path, FONT_SIZE)
        title_text = font.render("Super Bowser", True, COLORS["WHITE"])
        instructions_text = font.render("Press Enter to Start", True, COLORS["WHITE"])
        self.window.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        self.window.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2))


    def display_end_game(self):
        """
        Displays the end game screen with the game over message and score.
        """
        self.clear_level()

        self.window.fill(COLORS["BLACK"])
        font_path = os.path.join(os.path.dirname(__file__), FONT_PATH)
        font = pg.font.Font(font_path, FONT_SIZE)
        game_over_text = font.render("Game Over", True, COLORS["WHITE"])
        score_text = font.render(f"Score: {self.ui.score}", True, COLORS["WHITE"])
        instructions_text = font.render("Press Enter to play again", True, COLORS["WHITE"])
        self.window.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        self.window.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        self.window.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    
    def clear_level(self):
        """
        Clears the current game level by resetting the map, sprites, player, camera, observer, and audio players.
        """
        self.map = None
        self.all_sprites.empty()
        self.player = None
        self.camera = None
        self.observer = None
        self.audio_players = None
        self.delta_time = None
      

def update_display(game):
    """
    Updates the game display based on the current FSM state.
    """
    if game.fsm.current == game.playing:
        game.window.fill(COLORS["BACKGROUND"])
        game.map.draw(game.window, game.camera)

        for sprite in game.all_sprites:
            game.window.blit(sprite.image, game.camera.apply(sprite))
        game.ui.draw_labels(game.window)

    pg.display.flip()

def event_handler(running, game):
    """
    Handles game events such as key presses and custom game events.
    """
    for event in pg.event.get(): 
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN and game.fsm.current == game.game_over:
                game.ui.reset_labels_values()
                game.setup_game_level()
                game.fsm.update("restart_game", game)

            elif event.key == pg.K_RETURN and game.fsm.current == game.start_menu:
                game.setup_game_level()
                game.fsm.update("start_game", game)

        elif event.type == GAME_EVENTS["QUIT_GAME_EVENT"]:
            print("Quit game event triggered")
            running = False

        elif event.type == GAME_EVENTS["PLAYER_DEATH_EVENT"]: 
            game.audio_players[1].play("bowser_death")
            player = next(sprite for sprite in game.all_sprites if isinstance(sprite, Player))
            player.respawn()
            game.ui.update_score(-50)

        elif event.type == GAME_EVENTS["TIMEOUT_EVENT"]:
            game.clear_level()

            game.fsm.update("game_over", game)

            game.audio_players[0].stop()
            game.audio_players[1].play("game_over")

        elif event.type == GAME_EVENTS["TIME_ALERT_EVENT"]:
            game.ui.change_timer_text_color()
            game.audio_players[1].play("time_warning")

        elif event.type == GAME_EVENTS["PLAYER_JUMP_EVENT"]:
            game.audio_players[1].play("jump")

        elif event.type == GAME_EVENTS["END_GAME_EVENT"]:
            print("End of game")
            game.audio_players[0].stop()

            game.fsm.update("game_over", game)
        
        elif event.type == GAME_EVENTS["ENEMY_KILLED_EVENT"]:
            game.audio_players[1].play("enemy_killed")

            for sprite in game.all_sprites:
                if isinstance(sprite, Kirby) and sprite.dead: 
                    game.all_sprites.remove(sprite)

            game.ui.update_score(100)

    return running

def get_audio_players():
    """
    Initializes and returns the audio players for music and sound effects.
    """
    music_player = SoundPlayer(["overworld_theme", "game_over"], True)
    music_player.play("overworld_theme")
    sound_effecter = SoundPlayer(["jump","bowser_death","time_warning", "enemy_killed"], False)
    return [music_player, sound_effecter]

def game_loop(game):
    """
    Main game loop that handles the game states and updates the display.
    """
    running = True

    while running:
        if game.fsm.current == game.start_menu:
              game.display_start_menu()

        elif game.fsm.current == game.playing:
            game.play_level()

        elif game.fsm.current == game.game_over:
            game.display_end_game()

        running = event_handler(running,game)
        update_display(game)
        
    pg.quit()

def main():
    """
    Entry point for the game. Initializes the game and starts the game loop.
    """
    game = Game()
    game_loop(game)

if __name__ == "__main__":
    main()