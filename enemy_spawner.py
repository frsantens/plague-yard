import pygame
import random
from enemy import Enemy
from constants import *

class EnemySpawner:
    edges = [
        [pygame.Vector2(1, 0), lambda y: pygame.Vector2(-30, y * SCREEN_HEIGHT)],
        [pygame.Vector2(-1, 0), lambda y: pygame.Vector2(SCREEN_WIDTH + 30, y * SCREEN_HEIGHT)],
        [pygame.Vector2(0, 1), lambda x: pygame.Vector2(x * SCREEN_WIDTH, -30)],
        [pygame.Vector2(0, -1), lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + 30)],
    ]

    def __init__(self, player):
        self.spawn_timer = 0.0
        self.player = player
        self.last_player_level = player.level
        self.spawn_rate = 2.0 + (self.player.level * 0.2)  # More reasonable spawn rate

    def spawn(self, position, speed):
        return Enemy(position.x, position.y, speed)

    def update(self, dt, enemies):
        if self.player.level != self.last_player_level:
            self.spawn_rate = 2.0 + (self.player.level * 0.2)
            self.last_player_level = self.player.level

        self.spawn_timer += dt
        if self.spawn_timer >= 1.0 / self.spawn_rate:
            self.spawn_timer = 0.0

            edge = random.choice(self.edges)
            speed = random.randint(1, 3)
            position = edge[1](random.uniform(0, 1))
            enemies.append(self.spawn(position, speed))
