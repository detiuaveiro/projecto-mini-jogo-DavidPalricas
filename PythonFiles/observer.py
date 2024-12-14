import pygame as pg
import os
from consts import GAME_TIME, ALERT_TIME, TIMEOUT, GAME_SECOND, GAME_EVENTS


class Observer:
 """The Score class acts as game observer, because to update the score it needs to listen to the game events.
    This class is also responsible for drawing the score and timer labels on the screen.

      Attributes:
         - player (Player): The player object.
         - game_map (GameMap): The game map object.
         - score (int): The score of the player.
         - time (int): The time left in the game.
         - font (Font): The font object used for rendering the text on the screen
 """
 def __init__(self,player,game_map,enemies) -> None:
    """ Initializes a new instance of the Score class and sets up the attributes of the class.

         Args:
            - player (Player): The player object.
            - game_map (GameMap): The game map object.
    """
    self.player = player
    self.game_map = game_map
    self.enemies = enemies



    self.score = 0
    self.time = GAME_TIME
     
    font_path = os.path.join(os.path.dirname(__file__), "../Assets/Font/mario_nes.ttf")
    self.font = pg.font.Font(font_path, 12)


 def check_collisions(self):
   """ The check_collision function checks if the player has collided with any of the blocks in the game map.

      For now this method only checks if the player has collided with the brick blocks and question blocks in the game map, when the player is below the block.
      If the player has collided with a brick block, it breaks the block and adds 50 points to the player's score.
      If the player has collided with a question block, it replaces the block with a used question block.
   """

   if self.player.rect.collidelist(self.game_map.floor_blocks_colliders) != -1:
      block_index = self.player.rect.collidelist(self.game_map.floor_blocks_colliders)
      block = self.game_map.floor_blocks_colliders[block_index]
   
      if self.player.velocity_y > 0  and self.player.rect.bottom > block.top and self.player.rect.top < block.top:
   
        self.player.rect.bottom = block.top 

        self.player.on_block = None
  
        self.player.velocity_y = 0
   
        self.player.is_on_ground = True

   else:
          self.player.is_on_ground = False

   
   enemies_colliders = [enemy.rect for enemy in self.enemies]
   if self.player.rect.collidelist(enemies_colliders) != -1:

      enemy = self.enemies[self.player.rect.collidelist(enemies_colliders)]

      kirby_collider = enemies_colliders[self.player.rect.collidelist(enemies_colliders)]


      if self.player.rect.bottom >= kirby_collider.top and  not self.player.is_on_ground:
         enemy.dead = True

      else:
         self.player.rect.x = 0
         self.player.rect.y = 235
         self.score -= 100

 def draw_score_label(self,window):
    """ The draw_score_label function is responsible for drawing the score label on the screen.

         Args:
            - window (Surface): The game window object.
    """

    player_text = self.font.render("Bowser", True, (255,255,255))
    score_label = self.font.render(f"{self.score:07}", True, (255, 255, 255))

    window.blit(player_text, (10, 10))
    window.blit(score_label, (10, 25))


 def draw_timer_label(self,window, delta_time):
    """ The draw_timer_label function is responsible for drawing the timer label on the screen after 1 second has passed.
        It also changes the color of the timer label when the time is running out, and plays a warning sound effect and the version of the music speed up.
        It stops the music player and decremeting the time when the time is up.

         Args:
            - window (Surface): The game window object.
            - delta_time (int): The time elapsed since the last frame.
    """
 
    if self.time > TIMEOUT and delta_time >= GAME_SECOND :
        self.time -= 1

    time_label = self.font.render(f"TIME", True, (255, 255, 255))
    timer_label = self.font.render(f"{self.time:03}", True, (255, 255, 255))

    if self.time == ALERT_TIME:
       print(self.time)

       pg.event.post(pg.event.Event(GAME_EVENTS["TIME_ALERT_EVENT"]))

    elif self.time <= ALERT_TIME and self.time > TIMEOUT:
         timer_label = self.font.render(f"{self.time:03}", True, (255, 0, 0))

    elif self.time == TIMEOUT:
         pg.event.post(pg.event.Event("TIMEOUT_EVENT"))
         
    window.blit(time_label, (700, 10))
    window.blit(timer_label, (705, 25))

 def draw_ui_labels(self,window,delta_time):
    """ The draw_ui_labels function is responsible for calling the methods to draw the score and timer labels on the screen.

         Args:
            - window (Surface): The game window object.
            - delta_time (int): The time elapsed since the last frame.
    """
    self.draw_score_label(window)
    self.draw_timer_label(window,delta_time)
