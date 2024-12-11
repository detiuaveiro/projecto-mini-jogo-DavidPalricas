import pygame as pg

class Camera:
    _instance = None

    def __new__(cls, width, height):
        if cls._instance is None:
            cls._instance = super(Camera, cls).__new__(cls)
            cls._instance.__init__(width, height)
        return cls._instance

    def __init__(self, width, height):
        if not hasattr(self, 'initialized'):  # Ensure __init__ is only called once
            self.width = width
            self.height = height
            self.camera = pg.Rect(0, 0, width, height)
            # Define the tracking box (centered and smaller than the screen)
            self.tracking_box = pg.Rect(
                width // 4, height // 4, width // 2, height // 2
            )
            self.initialized = True

    def apply(self, target):
        """
        Adjust the target's rect or position by the camera offset.
        Can handle both entities with a rect attribute and standalone pygame.Rect objects.
        """
        if isinstance(target, pg.Rect):
            return target.move(self.camera.topleft)
        return target.rect.move(self.camera.topleft)

    def update(self, target):
        """
        Updates the camera position based on the player's position
        and the tracking box constraints.
        """
        if target.rect.left < self.tracking_box.left:
            self.camera.x -= self.tracking_box.left - target.rect.left  
        elif target.rect.right > self.tracking_box.right:
            self.camera.x += target.rect.right - self.tracking_box.right

        if target.rect.top < self.tracking_box.top:
            self.camera.y -= self.tracking_box.top - target.rect.top
        elif target.rect.bottom > self.tracking_box.bottom:
            self.camera.y += target.rect.bottom - self.tracking_box.bottom

        # Keep the camera within the bounds of the game world
        self.camera.x = max(0, min(self.camera.x, self.camera.width - self.width))
        self.camera.y = max(0, min(self.camera.y, self.camera.height - self.height))
