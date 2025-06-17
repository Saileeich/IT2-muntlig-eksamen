import pygame
from pygame.locals import *

from enemy import Enemy
from player import Player

class App:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.FPS = 24
        self.running = True
        self.colours = {
            "col1": (84, 73, 75),
            "col2": (241, 247, 237),
            "col3": (145, 199, 177),
            "col4": (179, 57, 81),
            "col5": (227, 208, 129),
            "col6": (176, 142, 162),
            "col7": (223, 154, 87)
        }
        self.entity_size = 10

        self.sprites = {
            "walls": pygame.sprite.Group(),
            "obstacles": pygame.sprite.Group(),
            "detection_cones": pygame.sprite.Group(),
            "enemies": pygame.sprite.Group(),
            "player": pygame.sprite.GroupSingle(),
        }

        self.events = {key: 0 for key in ["up", "down", "left", "right", "w", "a", "s", "d"]}

    def run(self):
        self.screen = pygame.display.set_mode((384, 576))
        pygame.display.set_caption("Snikespill")

        enemy1 = Enemy(self.entity_size, pygame.Vector2(320, 100), pygame.Vector2(320, 409), self.colours["col7"], self.colours["col4"], 3)
        self.sprites["detection_cones"].add(enemy1.detection_cone)
        self.sprites["enemies"].add(enemy1)

        enemy2 = Enemy(self.entity_size, pygame.Vector2(100, 100), pygame.Vector2(100, 200), self.colours["col7"], self.colours["col4"], 3.5, 5)
        self.sprites["detection_cones"].add(enemy2.detection_cone)
        self.sprites["enemies"].add(enemy2)

        self.sprites["player"].add(Player(self.entity_size, pygame.Vector2(200, 200), self.colours["col2"], 3))

        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(self.FPS)

        pygame.quit()

    def draw(self):
        # Fyller skjermen og tegner sprites på nytt
        self.screen.fill(self.colours["col1"])
        for sprite_group in self.sprites.values():
            sprite_group.draw(self.screen)

        """# Debug
        pygame.draw.rect(self.screen, (0,255,0), self.sprites["player"].sprite.rect, 2)
        for cone in self.sprites["detection_cones"]:
            pygame.draw.rect(self.screen, (255,255,0), cone.rect, 2)"""

        # Oppdater skjerm
        pygame.display.flip()

    def update(self):
        self.sprites["player"].update(self.events)
        self.sprites["enemies"].update()
        self.sprites["detection_cones"].update(self.sprites["player"])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.events["up"] = 1
                elif event.key == K_DOWN:
                    self.events["down"] = 1
                elif event.key == K_LEFT:
                    self.events["left"] = 1
                elif event.key == K_RIGHT:
                    self.events["right"] = 1
                elif event.key == K_w:
                    self.events["w"] = 1
                elif event.key == K_s:
                    self.events["s"] = 1
                elif event.key == K_a:
                    self.events["a"] = 1
                elif event.key == K_d:
                    self.events["d"] = 1
            elif event.type == KEYUP:
                if event.key == K_UP:
                    self.events["up"] = 0
                elif event.key == K_DOWN:
                    self.events["down"] = 0
                elif event.key == K_LEFT:
                    self.events["left"] = 0
                elif event.key == K_RIGHT:
                    self.events["right"] = 0
                elif event.key == K_w:
                    self.events["w"] = 0
                elif event.key == K_s:
                    self.events["s"] = 0
                elif event.key == K_a:
                    self.events["a"] = 0
                elif event.key == K_d:
                    self.events["d"] = 0
            elif event.type == QUIT:
                self.running = False