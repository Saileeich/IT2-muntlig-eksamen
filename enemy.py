import pygame
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, size: int = 16, position1: pygame.Vector2 = pygame.Vector2(0, 0), position2: pygame.Vector2 = pygame.Vector2(0, 0), idle_colour: tuple = (200, 200, 200), alerted_colour: tuple = (255, 0, 0), speed: float = 1.0, rotation_speed: int = 3):
        if position1 == position2:
            raise ValueError("Start og sluttposisjon kan ikke være like")
        
        super().__init__()
        
        self.move_points = [position1, position2]
        self.move_state = 0
        self.target = position2
        self.speed = speed
        self.size = size
        self.colour = idle_colour
        self.alerted_colour = alerted_colour

        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, self.colour, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(topleft=position1)
        
        self.rotation = math.degrees(math.acos((position2.x - position1.x) / (position2 - position1).length()))
        self.start_rotation = self.rotation
        self.rotating = False
        self.rotation_speed = rotation_speed

        self.detection_cone = DetectionCone(self, 6*self.size, 60, self.alerted_colour)
        self.detection = 0
        self.detection_threshold = 10

    def update(self):
        if self.rotating:
            if self.rotation != self.start_rotation+180:
                self.rotation += self.rotation_speed
            else:
                self.start_rotation = self.rotation
                self.rotating = False
        else:
            if pygame.math.Vector2(self.rect.topleft).distance_to(self.target) < 1:
                self.target = self.move_points[self.move_state]
                self.move_state = not self.move_state
                self.rotating = True
            else:
                self.rect.topleft = pygame.math.Vector2.move_towards(pygame.Vector2(self.rect.topleft), self.target, self.speed)

        self.image.fill((0, 0, 0, 0))
        new_colour = (
            self.colour[0] + ((self.alerted_colour[0]-self.colour[0])/self.detection_threshold) * self.detection,
            self.colour[1] + ((self.alerted_colour[1]-self.colour[1])/self.detection_threshold) * self.detection,
            self.colour[2] + ((self.alerted_colour[2]-self.colour[2])/self.detection_threshold) * self.detection
        )
        pygame.draw.circle(self.image, new_colour, (self.size // 2, self.size // 2), self.size // 2)

        self.detection -= 0.03
        if self.detection < 0:
            self.detection = 0

    def increase_detection(self, amount: float = 1):
        self.detection += amount
        if self.detection > self.detection_threshold:
            self.detection = self.detection_threshold
            
            # Lag egen event
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"player_detected": self}))


class DetectionCone(pygame.sprite.Sprite):
    def __init__(self, enemy: Enemy, radius: float = 30, detection_angle: float = 50, colour: tuple = (255, 0, 0, 128)):
        super().__init__()
        self.enemy = enemy
        self.radius = radius
        self.detection_angle = detection_angle
        self.colour = colour
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=enemy.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, collision_group: pygame.sprite.GroupSingle):
        self.image.fill((0, 0, 0, 0))

        center = pygame.Vector2(self.radius, self.radius)
        angle1 = self.enemy.rotation + self.detection_angle / 2
        angle2 = self.enemy.rotation - self.detection_angle / 2
        p1 = center
        p2 = pygame.Vector2(
            self.radius * math.cos(math.radians(angle1)),
            self.radius * math.sin(math.radians(angle1))
        ) + center
        p3 = pygame.Vector2(
            self.radius * math.cos(math.radians(angle2)),
            self.radius * math.sin(math.radians(angle2))
        ) + center

        pygame.draw.polygon(
            self.image, (self.colour[0], self.colour[1], self.colour[2], 128), [p1, p2, p3]
        )

        self.rect = self.image.get_rect(center=self.enemy.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

        collided = pygame.sprite.spritecollide(self, collision_group, False, pygame.sprite.collide_mask)
        if collided:
            self.enemy.increase_detection(1.2)