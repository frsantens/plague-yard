import pygame
from constants import *

class Player():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.color = BLUE
        self.level = 1
        self.health = 20
        self.speed = 4
        self.attack = 5
        self.defence = 1
        self.dodge = 0.05
        self.stats = [
            f'level: {self.level}',
            f'health: {self.health}'
        ]

        # temp to draw square
        self.size = 35

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def move(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_DOWN]:
            dy += 1
        
        # Normalize diagonal movement
        if dx != 0 or dy != 0:
            magnitude = (dx**2 + dy**2)**0.5
            dx = (dx / magnitude) * self.speed
            dy = (dy / magnitude) * self.speed
        self.x += dx
        self.y += dy
        
        # Keep player within screen bounds
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))
