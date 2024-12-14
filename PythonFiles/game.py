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
            self.map = Map()
            self.fsm = fsm.FSM(self.set_states(), self.set_transitions())
            self.__initialized = True

    def setup_pygame(self):
        pg.init()
        window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Super Bowser")
        clock = pg.time.Clock()

        return window, clock
    
    def set_states(self):
        self.start_menu = fsm.StartMenu()
        self.playing = fsm.Playing()
        self.game_over = fsm.GameOver()

        return [self.start_menu, self.playing, self.game_over]
    
    def set_transitions(self):
        return {
            "start_game": fsm.Transition(self.start_menu, self.playing),
            "game_over": fsm.Transition(self.playing, self.game_over),
            "restart_game": fsm.Transition(self.game_over, self.start_menu)
        }

    def reset_game(self):
        self.map = Map()
        self.fsm.update("start_game", self)

def display_start_menu(window):
    window.fill(COLORS["BLACK"])
    font_path = os.path.join(os.path.dirname(__file__), FONT_PATH)
    font = pg.font.Font(font_path, FONT_SIZE)
    title_text = font.render("Super Bowser", True, COLORS["WHITE"])
    instructions_text = font.render("Press Enter to Start", True, COLORS["WHITE"])
    window.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    window.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pg.display.flip()

def display_end_game(window, game_ui):
    window.fill(COLORS["BLACK"])
    font_path = os.path.join(os.path.dirname(__file__), FONT_PATH)
    font = pg.font.Font(font_path, FONT_SIZE)
    game_over_text = font.render("Game Over", True, COLORS["WHITE"])
    score_text = font.render(f"Score: {game_ui.score}", True, COLORS["WHITE"])
    instructions_text = font.render("Press Enter to play again", True, COLORS["WHITE"])
    window.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    window.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    window.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    pg.display.flip()

def update_display(all_sprites, window, game_map, game_ui, camera):
    window.fill(COLORS["BACKGROUND"])  
    game_map.draw(window, camera)
    for sprite in all_sprites:
        window.blit(sprite.image, camera.apply(sprite))
    game_ui.draw_labels(window)
    pg.display.flip()

def event_handler(running, audio_players, all_sprites, window, game_ui, game):
    for event in pg.event.get():  
        if event.type == pg.QUIT:
            running = False
        elif event.type == GAME_EVENTS["QUIT_GAME_EVENT"]:
            print("Quit game event triggered")
            running = False
        elif event.type == GAME_EVENTS["PLAYER_DEATH_EVENT"]: 
            audio_players[1].play("bowser_death")
            player = next(sprite for sprite in all_sprites if isinstance(sprite, Player))
            player.respawn()
            game_ui.update_score(-50)
        elif event.type == GAME_EVENTS["TIMEOUT_EVENT"]:
            game.fsm.update("game_over", game)
            audio_players[0].stop()
            audio_players[1].play("game_over")
        elif event.type == GAME_EVENTS["TIME_ALERT_EVENT"]:
            game_ui.change_timer_text_color()
            audio_players[1].play("time_warning")
        elif event.type == GAME_EVENTS["PLAYER_JUMP_EVENT"]:
            audio_players[1].play("jump")
        elif event.type == GAME_EVENTS["END_GAME_EVENT"]:
            print("End of game")
            audio_players[0].stop()
            display_end_game(window, game_ui)
            waiting = True
            while waiting:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                        waiting = False
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_RETURN:
                            game.reset_game()
                            waiting = False
        elif event.type == GAME_EVENTS["ENEMY_KILLED_EVENT"]:
            audio_players[1].play("enemy_killed")
            for sprite in all_sprites:
                if isinstance(sprite, Kirby) and sprite.dead: 
                    all_sprites.remove(sprite)
            game_ui.update_score(100)
    return running, all_sprites

def get_audio_players():
    music_player = SoundPlayer(["overworld_theme", "game_over"], True)
    music_player.play("overworld_theme")
    sound_effecter = SoundPlayer(["jump","bowser_death","time_warning", "enemy_killed"], False)
    return [music_player, sound_effecter]

def game_loop(game):
    running = True
    window, clock, game_map = game.window, game.clock, game.map
    all_sprites = setup_sprites()  
    player = next(sprite for sprite in all_sprites if isinstance(sprite, Player)) 
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
    observer = Observer()
    audio_players = get_audio_players()
    delta_time = 0
    game_ui = UI()
    while running:
        if game.fsm.current == game.start_menu:
            display_start_menu(window)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        game.fsm.update("start_game", game)
        elif game.fsm.current == game.playing:
            running, all_sprites = event_handler(running, audio_players, all_sprites, window, game_ui, game)
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
            window.fill(COLORS["BLACK"])
            pg.display.flip()
            pass
    pg.quit()

def setup_sprites():
    all_sprites = pg.sprite.Group()
    player = Player((0,235,25,31)) 
    all_sprites.add(player)
    kirby = Kirby((150, 252, 18, 20))
    all_sprites.add(kirby)
    kirby2 = Kirby((350, 252, 18, 20))
    all_sprites.add(kirby2)
    kirby3 = Kirby((570, 195, 18, 20))
    all_sprites.add(kirby3)
    kirby4 = Kirby((770, 138, 18, 20))
    all_sprites.add(kirby4)
    kirby5 = Kirby((1000, 195, 18, 20))
    all_sprites.add(kirby5)
    return all_sprites

def main():
    game = Game()
    game_loop(game)

if __name__ == "__main__":
    main()