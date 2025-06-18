import pygame
from pygame.locals import *
import json

from enemy import Enemy
from player import Player
from tile import Tile

class App:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font("assets/fonts/PixeloidMono.ttf", 16)

        self.clock = pygame.time.Clock()
        self.FPS = 24
        self.tile_size = 20
        self.WIDTH, self.HEIGHT = self.tile_size*20, self.tile_size*30
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
        self.level = 0

        self.events = {key: 0 for key in ["up", "down", "left", "right", "w", "a", "s", "d", "lshift", "r"]}

        self.playing = False
        self.boot = True
        self.game_over = False
        self.victory = False
        self.boot_time = 5000
        

    def run(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snikespill")

        while self.running:
            self.handle_events()

            if self.playing:
                self.game_loop()
            elif self.game_over:
                self.game_over_loop()
            elif self.victory:
                self.victory_loop()
            elif self.boot:
                self.boot_loop()
            else:
                raise Exception("Invalid game state")

            self.clock.tick(self.FPS)

        pygame.quit()

    def boot_loop(self):
        self.screen.fill((0,0,0))
        hampter = pygame.image.load("assets/images/hampter.png")
        hampter = pygame.transform.scale(hampter, (self.WIDTH, self.WIDTH/hampter.get_width() * hampter.get_height()))
        hampter.set_alpha(pygame.time.get_ticks() * (255/(self.boot_time*0.75)))  # Fade in effect
        self.screen.blit(hampter, pygame.Vector2(self.WIDTH/2 - hampter.get_width()/2, self.HEIGHT/2 - hampter.get_height()/2))
        pygame.display.flip()

        if pygame.time.get_ticks() > self.boot_time:
            self.boot = False
            self.start_game()

    def game_loop(self):
        self.update()
        self.draw()

    def game_over_loop(self):
        if self.events["r"]:
            self.game_over = False
            self.level = 0
            self.start_game()

    def victory_loop(self):
        if self.events["r"]:
            self.victory = False
            self.level += 1
            self.start_game()

    def start_game(self):
        self.playing = True

        self.sprites = {
            "victory_tiles": pygame.sprite.Group(),
            "obstacles": pygame.sprite.Group(),
            "detection_cones": pygame.sprite.Group(),
            "enemies": pygame.sprite.Group(),
            "player": pygame.sprite.GroupSingle(),
        }

        self.load_level(self.level)

    def load_level(self, id: int):
        with open("assets/level.json", "r") as file:
            level_data = json.load(file)[id]

            player = Player(self.tile_size, pygame.Vector2(level_data["player"]["x"] * self.tile_size, level_data["player"]["y"] * self.tile_size), self.colours["col2"], level_data["player"]["speed"])
            self.sprites["player"].add(player)

            for enemy_data in level_data["enemies"]:
                enemy = Enemy(self.tile_size, pygame.Vector2(enemy_data["position_a"]["x"] * self.tile_size, enemy_data["position_a"]["y"] * self.tile_size), pygame.Vector2(enemy_data["position_b"]["x"] * self.tile_size, enemy_data["position_b"]["y"] * self.tile_size), self.colours["col7"], self.colours["col4"], enemy_data["speed"], enemy_data["rotation_speed"])
                self.sprites["enemies"].add(enemy)
                self.sprites["detection_cones"].add(enemy.detection_cone)

            for obstacle_data in level_data["obstacles"]:
                obstacle = Tile(self.tile_size, pygame.Vector2(obstacle_data["position"]["x"] * self.tile_size, obstacle_data["position"]["y"] * self.tile_size), self.colours["col6"])
                self.sprites["obstacles"].add(obstacle)

            for victory_tile_data in level_data["victory_tiles"]:
                victory_tile = Tile(self.tile_size, pygame.Vector2(victory_tile_data["position"]["x"] * self.tile_size, victory_tile_data["position"]["y"] * self.tile_size), self.colours["col3"])
                self.sprites["victory_tiles"].add(victory_tile)



    def draw(self):
        # Fyller skjermen og tegner sprites på nytt
        self.screen.fill(self.colours["col1"])

        for sprite_group in self.sprites.values():
            sprite_group.draw(self.screen)

        # Visualiserer rekkevidden for sprint lyden
        if self.events["lshift"]:
            pygame.draw.circle(self.screen, self.colours["col2"], (self.sprites["player"].sprite.rect.centerx, self.sprites["player"].sprite.rect.centery), self.tile_size*11.5, 1)
        else:
            pygame.draw.circle(self.screen, self.colours["col2"], (self.sprites["player"].sprite.rect.centerx, self.sprites["player"].sprite.rect.centery), self.tile_size*2.5, 1)

        """# Debug
        pygame.draw.rect(self.screen, (0,255,0), self.sprites["player"].sprite.rect, 2)
        for cone in self.sprites["detection_cones"]:
            pygame.draw.rect(self.screen, (255,255,0), cone.rect, 2)"""

        # Oppdater skjerm
        pygame.display.flip()

    def update(self):
        self.sprites["player"].update(self.events, self.sprites)
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
                elif event.key == K_LSHIFT:
                    self.events["lshift"] = 1
                elif event.key == K_r:
                    self.events["r"] = 1
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
                elif event.key == K_LSHIFT:
                    self.events["lshift"] = 0
                elif event.key == K_r:
                    self.events["r"] = 0
            elif event.type == USEREVENT:
                if "player_detected" in event.dict:
                    if self.playing:
                        self.game_over = True
                        self.playing = False
                        for enemy in self.sprites["enemies"]:
                            enemy.detection = enemy.detection_threshold
                        
                        text1 = self.font.render("DU BLE OPPDAGET!", True, (255, 0, 0), (0, 0, 0))
                        self.screen.blit(text1, (self.WIDTH/2 - text1.get_width()/2, self.HEIGHT/2 - text1.get_height()/2))
                        text2 = self.font.render("TRYKK PÅ 'R' FOR Å PRØVE IGJEN", True, (255, 255, 255), (0, 0, 0))
                        self.screen.blit(text2, (self.WIDTH/2 - text2.get_width()/2, self.HEIGHT/2 - text2.get_height()/2 + 30))
                        pygame.display.flip()
                elif "player_won" in event.dict:
                    if self.playing:
                        self.victory = True
                        self.playing = False
                        text1 = self.font.render("DU VANT!", True, (0, 255, 0), (0, 0, 0))
                        self.screen.blit(text1, (self.WIDTH/2 - text1.get_width()/2, self.HEIGHT/2 - text1.get_height()/2))
                        text2 = self.font.render("TRYKK PÅ 'R' FOR Å FORTSETTE", True, (255, 255, 255), (0, 0, 0))
                        self.screen.blit(text2, (self.WIDTH/2 - text2.get_width()/2, self.HEIGHT/2 - text2.get_height()/2 + 30))
                        pygame.display.flip()
            elif event.type == QUIT:
                self.running = False