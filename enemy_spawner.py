import pygame as pg
import random
from enemy import *
from constants import *
import inspect

class EnemySpawner:
    def __init__(self, player):
        self.spawn_timer = 0.0
        self.player = player
        self.last_player_level = player.level
        self.spawn_rate = SPAWN_RATE + (self.player.level * SPAWN_RATE_MULT) 
        # Automatically get all Enemy subclasses and their enemy_types
        self.enemy_classes = self._get_enemy_classes()
        self.enemy_types = list(self.enemy_classes.keys())
        self.enemy_weights = [self.enemy_classes[enemy_type].spawn_weight for enemy_type in self.enemy_types]

    def _get_enemy_classes(self):
        """Get all Enemy subclasses and map them by their enemy_type"""
        enemy_classes = {}
        for name, obj in globals().items():
            if (inspect.isclass(obj) and 
                issubclass(obj, Enemy) and 
                obj != Enemy):
                # Create temporary instance to get enemy_type
                temp_instance = obj(0, 0, 1)
                enemy_classes[temp_instance.enemy_type] = obj
        return enemy_classes

    def get_random_spawn_position(self, enemy_type):
        edge = random.randint(0, 3)  # 0=left, 1=right, 2=top, 3=bottom
        sw = SCREEN_WIDTH
        sh = SCREEN_HEIGHT
        # Get the size of the enemy type that is chosen to spawn
        temp_enemy = self.enemy_classes[enemy_type](0, 0, 1)
        offset = temp_enemy.size + 50  # Add some extra buffer
        if edge == 0:  # left
            return pg.Vector2(-offset, random.uniform(0, sh))
        elif edge == 1:  # right
            return pg.Vector2(sw + offset, random.uniform(0, sh))
        elif edge == 2:  # top
            return pg.Vector2(random.uniform(0, sw), -offset)
        else:  # bottom
            return pg.Vector2(random.uniform(0, sw), sh + offset)

    def spawn(self, position, enemy_type, speed):
        # Dynamic spawning using the enemy_classes dictionary
        enemy_class = self.enemy_classes[enemy_type]
        return enemy_class(position.x, position.y, speed)

    def update(self, dt, enemies):
        if self.player.level != self.last_player_level:
            self.spawn_rate = 2.0 + (self.player.level * 0.4)
            self.last_player_level = self.player.level
        self.spawn_timer += dt
        if self.spawn_timer >= 1.0 / self.spawn_rate:
            enemy_type = random.choices(
                self.enemy_types, weights=self.enemy_weights
                )[0]
            position = self.get_random_spawn_position(enemy_type)
            speed = random.uniform(1, 4)
            enemies.append(self.spawn(position, enemy_type, speed))
            self.spawn_timer = 0.0
