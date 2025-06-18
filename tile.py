import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, size: int = 32, position: pygame.Vector2 = pygame.Vector2(0, 0), colour: tuple = (255, 0, 0), source: str = None):
        super().__init__()
        
        self.size = size
        self.position = position
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        if source is None:
            self.image.fill(colour)
        else:
            self.image = pygame.transform.scale(pygame.image.load(source).convert_alpha(), (size, size))
        self.rect = self.image.get_rect(topleft=self.position)
        self.mask = pygame.mask.from_surface(self.image)