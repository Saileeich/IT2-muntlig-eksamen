import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, size: int = 32, position: pygame.Vector2 = pygame.Vector2(0, 0), colour: tuple = (255, 255, 255), speed: float = 5):
        super().__init__()
        self.position = position
        self.speed = speed
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        #self.image.fill((255, 255, 255))
        pygame.draw.circle(self.image, colour, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(topleft=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, events: dict):
        horizontal_move = (events["right"] or events["d"]) - (events["left"] or events["a"])
        vertical_move = (events["down"] or events["s"]) - (events["up"] or events["w"])


        screen_width, screen_height = pygame.display.get_window_size()

        if self.position.x + horizontal_move * self.speed < 0 or self.position.x + horizontal_move * self.speed > screen_width - self.rect.width:
            horizontal_move = 0

        if self.position.y + vertical_move * self.speed < 0 or self.position.y + vertical_move * self.speed > screen_height - self.rect.height:
            vertical_move = 0


        move = pygame.Vector2(horizontal_move, vertical_move).normalize() * self.speed if horizontal_move or vertical_move else pygame.Vector2(0, 0)
        self.position += move

        self.rect.topleft = self.position
        self.mask = pygame.mask.from_surface(self.image)