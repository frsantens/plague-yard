import pygame
import random

class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.color = (255, 0, 0)
        self.speed = random.randint(2, 4)
        self.attack = random.randint(5, 10)
        self.defense = random.randint(1, 3)
        self.cooldown = random.randint(30, 60)  # Attack cooldown in frames
        self.enemy_type = enemy_type

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move_towards_player(self, player):
        if self.x < player.x:
            self.x += self.speed
        elif self.x > player.x:
            self.x -= self.speed

        if self.y < player.y:
            self.y += self.speed
        elif self.y > player.y:
            self.y -= self.speed

    def attack_player(self, player):
        # Attack logic
        pass

class SlowStrongEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="SlowStrong")
        self.speed = 1
        self.attack = 20
        self.defense = 10

class FastWeakEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="FastWeak")
        self.speed = 6
        self.attack = 5
        self.defense = 2
