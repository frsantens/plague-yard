import pygame
import random
from enemy import SlowStrongEnemy, FastWeakEnemy
from constants import *

class EnemySpawner:
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ENEMY_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ENEMY_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ENEMY_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ENEMY_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self, player):
        self.spawn_timer = 0.0
        self.spawn_rate = 5.0  # Base spawn rate (enemies per second)
        self.player = player

    def spawn(self, position, velocity):
        enemy_type = random.choice([SlowStrongEnemy, FastWeakEnemy])
        return enemy_type(position.x, position.y)

    def update(self, dt, enemies):
        self.spawn_timer += dt
        if self.spawn_timer > 1 / self.spawn_rate:
            self.spawn_timer = 0
            self.spawn_rate = 5.0 + (self.player.level * 0.5)  # Increase spawn rate with player level

            # spawn a new enemy at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            enemies.append(self.spawn(position, velocity))
