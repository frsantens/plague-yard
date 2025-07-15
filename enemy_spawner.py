import pygame
import random
from enemy import *
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
        self.spawn_rate = 2.0 + (self.player.level * 0.2) 
        self.enemy_types = ["SlowStrong", "FastWeak", "Standard"]

    def spawn(self, position, enemy_type, speed):
        if enemy_type == "SlowStrong":
            return SlowStrongEnemy(position.x, position.y, speed)
        if enemy_type == "Standard":
            return StandardEnemy(position.x, position.y, speed)
        if enemy_type == "FastWeak":
            return FastWeakEnemy(position.x, position.y, speed)

    def update(self, dt, enemies):
        if self.player.level != self.last_player_level:
            self.spawn_rate = 2.0 + (self.player.level * 0.4)
            self.last_player_level = self.player.level

        self.spawn_timer += dt
        if self.spawn_timer >= 1.0 / self.spawn_rate:
            self.spawn_timer = 0.0

            edge = random.choice(self.edges)
            speed = random.uniform(1, 4)
            position = edge[1](random.uniform(0, 1))
            enemy_type = random.choice(self.enemy_types)
            enemies.append(self.spawn(position, enemy_type, speed))
