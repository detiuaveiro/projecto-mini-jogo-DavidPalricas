import pygame

class Camera:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Camera, cls).__new__(cls)
        return cls._instance

    def __init__(self, width, height):
        """Initialize camera"""
        if not hasattr(self, 'initialized'):  # Ensure __init__ is only called once
            self.camera = pygame.Rect(0, 0, width, height)
            self.width = width
            self.height = height
            self.initialized = True

    def apply(self, entity):
        """Apply camera offset to an entity"""
        if isinstance(entity, pygame.Rect):
            return entity.move(self.camera.topleft)
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        """Apply camera offset to a rectangle"""
        return rect.move(self.camera.topleft)

    def update(self, target):
        """Update camera position to follow target"""
        # Center the camera on the target
        x = -target.rect.centerx + self.width // 2
        y = -target.rect.centery + self.height // 2

        # Limit scrolling to map boundaries
        x = min(0, x)  # Left boundary
        y = min(0, y)  # Top boundary
        
        # Assuming a large map width and height - adjust these as needed
        map_width = 2000  # Example map width
        map_height = 277  # Example map height
        x = max(-(map_width - self.width), x)  # Right boundary
        y = max(-(map_height - self.height), y)  # Bottom boundary

        self.camera = pygame.Rect(x, y, self.width, self.height)