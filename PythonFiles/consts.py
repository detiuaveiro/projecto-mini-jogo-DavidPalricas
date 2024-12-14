import pygame as pg


# Game Event Constants
GAME_EVENTS = {"QUIT_GAME_EVENT": pg.USEREVENT + 1, 
               "PLAYER_DEATH_EVENT": pg.USEREVENT + 2, 
               "TIMEOUT_EVENT": pg.USEREVENT + 3, 
               "TIME_ALERT_EVENT": pg.USEREVENT + 4, 
               "PLAYER_JUMP_EVENT": pg.USEREVENT + 5, 
               "END_GAME_EVENT": pg.USEREVENT + 6, 
               "ENEMY_KILLED_EVENT": pg.USEREVENT + 7 
               }

# Screen SIze Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 277

# Map Constants flor block constants and peach sprite path
FLOOR_TILE_WIDTH = 16
FLOOR_TILE_HEIGHT = 19
FLOOR_BLOCK = 0
FLOOR_BLOCK_SPRITE_PATH = "../Assets/SpriteSheets/Map/floor_block.png"
PEACH_SPRITE_PATH = "../Assets/SpriteSheets/Peach/peach.png"

# Time Constants
GAME_TIME = 60
ALERT_TIME = 20
TIMEOUT = 0
GAME_SECOND = 1000

FPS = 60
GRAVITY = 0.8

# Player Constants
PLAYER_SPEED = 1.8
SPRINT_SPEED = PLAYER_SPEED * 2
PLAYER_JUMP_SPEED = 10
PLAYER_JUMP_SPEED_SPRINT = PLAYER_JUMP_SPEED * 1.5
PLAYER_FRICTION = 0.8
PLAYER_IDLE_SPRITE_PATH = "../Assets/SpriteSheets/Bowser/idle/bowser_idle.png"

# Kirby Constants
KIRBY_IDLE_SPRITE_PATH = "../Assets/SpriteSheets/Enemies/Kirby/idle/kirby_idle.png"
KIRBY_SPEED = 1.2
KIRBY_PATROL_MAX_DISTANCE = 100


# UI Constants
FONT_PATH = "../Assets/Font/mario_nes.ttf"
FONT_SIZE = 12
COLORS = {"WHITE": (255, 255, 255), "RED": (255, 0, 0)}
