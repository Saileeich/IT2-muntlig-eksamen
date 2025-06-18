import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, size: int = 32, position: pygame.Vector2 = pygame.Vector2(0, 0), colour: tuple = (255, 0, 0)):
        super().__init__()
        
        self.size = size
        self.position = position
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.fill(colour)
        self.rect = self.image.get_rect(topleft=self.position)
        self.mask = pygame.mask.from_surface(self.image)