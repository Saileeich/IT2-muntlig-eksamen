import pygame
from enemy import Enemy

class Player(pygame.sprite.Sprite):
    def __init__(self, size: int = 32, position: pygame.Vector2 = pygame.Vector2(0, 0), colour: tuple = (255, 255, 255), speed: float = 5, sprint_multiplier: float = 2):
        super().__init__()
        self.size = size
        self.position = position
        self.speed = speed
        self.sprint_multiplier = sprint_multiplier
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        #self.image.fill((255, 255, 255))
        pygame.draw.circle(self.image, colour, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(topleft=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, events: dict, sprite_groups: dict):
        # Enkel løsning for å vite hvilke retninger som er trykket ned
        horizontal_move = (events["right"] or events["d"]) - (events["left"] or events["a"])
        vertical_move = (events["down"] or events["s"]) - (events["up"] or events["w"])

        # Sett fart, og øk hvis man sprinter
        speed = self.speed
        if events["lshift"]:
            # Sprinting
            speed *= self.sprint_multiplier
            
        # Normaliser move vektoren og skjekk etter "kollisjon" med kantene
        move = pygame.Vector2(horizontal_move, vertical_move).normalize() * speed if horizontal_move or vertical_move else pygame.Vector2(0, 0)
        screen_width, screen_height = pygame.display.get_window_size()

        if self.position.x + move[0] < 0 or self.position.x + move[0] > screen_width - self.rect.width:
            move[0] = 0

        if self.position.y + move[1] < 0 or self.position.y + move[1] > screen_height - self.rect.height:
            move[1] = 0

        # Oppdater posisjon
        self.position += move

        # Oppdater rect og mask
        self.rect.topleft = self.position
        self.mask = pygame.mask.from_surface(self.image)


        # Sjekk for kollisjon med hindringer
        if pygame.sprite.spritecollideany(self, sprite_groups["obstacles"]):
            closest_enemy = self.get_closest_entity(sprite_groups["enemies"])
            closest_enemy.detection = closest_enemy.detection_threshold
            closest_enemy.increase_detection()

        # Sjekk om spiller er i mål
        if pygame.sprite.spritecollideany(self, sprite_groups["victory_tiles"]):
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"player_won": True}))


        for enemy in sprite_groups["enemies"]:
            distance = self.position.distance_to(enemy.rect.topleft)
            if distance <= self.size:
                # Hvis man kommer borti fienden, taper man
                enemy.detection = enemy.detection_threshold
                enemy.increase_detection(1)
            elif distance < self.size * 3 and move.length() > 0:
                # Hvis man går for nærme fienden, økes detection
                enemy.increase_detection(0.5)
            elif distance < self.size * 12 and events["lshift"] and move.length() > 0:
                # Hvis man sprinter for nærme fienden, økes detection
                enemy.increase_detection(0.5)
        
    def get_closest_entity(self, entity_group: pygame.sprite.Group):
        closest = None
        distance = float('inf')
        for entity in entity_group:
            difference = self.position - entity.rect.topleft
            if difference.length() < distance:
                distance = difference.length()
                closest = entity

        return closest