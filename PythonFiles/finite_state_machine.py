import pygame as pg
import os

class State:
    def __init__(self, name) -> None:
        self.name = name

    def enter(self):
        print(f"Entering {self.name}")

    def update(self, object):
        pass

    def exit(self):
     pass

    def get_sprite(self):
        return self.image

class Transition:
    def __init__(self, _from, _to) -> None:
        self._from = _from
        self._to = _to

class Idle(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object):
        print("waiting for your command...")
        return super().update(object)

class Walk(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object):
        print("Moving")
        return super().update(object)
    
class Jump(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object):
        print("Jumping")
        return super().update(object)
    

class FSM:
    def __init__(self, states: list[State], transitions: dict[Transition]) -> None:
        self._states = states
        self._transitions = transitions
        self.current_animation = "idle"
        self.current: State = self._states[0]
        self.end: State = self._states[-1]
        self.last_update = pg.time.get_ticks()
        self.animation_index = 0
        self.animation_delay = 20
        self.frames_number = 5
        self.animations_frames = None


    def update(self, event, object):
        if event:
            trans = self._transitions.get(event)
            if trans and trans._from == self.current:
                self.current.exit()
                self.current = trans._to
                self.play_animation(self.current.name,object)
                self.current.enter()
        self.current.update(object)

        if self.current == self.end:
            self.current.exit()
            return False
        return True
    
    def play_animation(self,state,entity):
     # Check if the current animation is different from the new animation
     if self.current_animation != state:
        self.current_animation = state
        self.animation_index = 0  # Reset the animati
        self.last_update = 0
        self.animations_frames = self.load_animation_frames(entity, state)
     
     # Get the current time in milliseconds since Pygame was initialized
     now = pg.time.get_ticks()
    
    # Check if the time elapsed since the last update is greater than the animation delay
     if now - self.last_update > self.animation_delay:
        # Update the last update time to the current time
        self.last_update = now
        
        # Increment the animation index and wrap it around using modulo to stay within the valid range
        self.animation_index = (self.animation_index + 1) % len(self.animations_frames)
        
        entity.image = self.animations_frames[self.animation_index]

        if not entity.turned_right:
            entity.image = pg.transform.flip(entity.image, True, False)
    



    def load_animation_frames(self, entity, state):
        """ Load the animation frames for the given state """
        sprite_width = entity.image.get_width()
        new_image = pg.image.load(os.path.join(os.path.dirname(__file__), f"../Assets/SpriteSheets/{entity.name}/{state}/{entity.name}_{state}.png")).convert_alpha()
        
        # Check if the image is a tileset
        if new_image.get_width() > sprite_width:
            return self.split_tileset(new_image, sprite_width)
        else:
            return [new_image]

    def split_tileset(self, tile_set, sprite_width):
        """ Split the tileset into individual frames """
        frames = []
        num_frames = tile_set.get_width() // sprite_width
        print(num_frames)

        for i in range(num_frames):
            frame = tile_set.subsurface((i * sprite_width, 0, sprite_width, tile_set.get_height()))
            frames.append(frame)
            

        return frames
