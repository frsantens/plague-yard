import pygame
from constants import *

class Enemy():
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.size = 30
        self.color = ORANGE
        self.speed = speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def move_towards_player(self, player):
        # Calculate direction vector
        dx = player.x - self.x
        dy = player.y - self.y
        
        # Calculate distance
        distance = (dx**2 + dy**2)**0.5
        
        # Normalize and apply speed
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed



