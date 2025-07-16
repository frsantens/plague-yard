import pygame as pg
import random
from enemy import SlowStrongEnemy, FastWeakEnemy, StandardEnemy, BossEnemy
from constants import *

class EnemySpawner:
    def __init__(self, player):
        self.spawn_timer = 0.0
        self.player = player
        self.last_player_level = player.level
        self.spawn_rate = 2.0 + (self.player.level * 0.2) 
        self.enemy_types = ["SlowStrong", "FastWeak", "Standard", "Boss"] 

    def get_random_spawn_position(self):
        edge = random.randint(0, 3)  # 0=left, 1=right, 2=top, 3=bottom
        sw = SCREEN_WIDTH
        sh = SCREEN_HEIGHT
        if edge == 0:  # left
            return pg.Vector2(-30, random.uniform(0, sh))
        elif edge == 1:  # right
            return pg.Vector2(sw + 30, random.uniform(0, sh))
        elif edge == 2:  # top
            return pg.Vector2(random.uniform(0, sw), -30)
        else:  # bottom
            return pg.Vector2(random.uniform(0, sw), sh + 30)

    def spawn(self, position, enemy_type, speed):
        if enemy_type == "SlowStrong":
            return SlowStrongEnemy(position.x, position.y, speed)
        if enemy_type == "Standard":
            return StandardEnemy(position.x, position.y, speed)
        if enemy_type == "FastWeak":
            return FastWeakEnemy(position.x, position.y, speed)
        if enemy_type == "Boss":
            return BossEnemy(position.x, position.y, speed)

    def update(self, dt, enemies):
        if self.player.level != self.last_player_level:
            self.spawn_rate = 2.0 + (self.player.level * 0.4)
            self.last_player_level = self.player.level
        self.spawn_timer += dt
        if self.spawn_timer >= 1.0 / self.spawn_rate:
            position = self.get_random_spawn_position()
            speed = random.uniform(1, 4)
            enemy_type = random.choices(
                self.enemy_types, weights=[10,20,40,1]
                )[0]
            enemies.append(self.spawn(position, enemy_type, speed))
            self.spawn_timer = 0.0
