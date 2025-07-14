import pygame
from constants import *

class Enemy():
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.size = 30
        self.center = (self.x + self.size//2, self.y + self.size//2)
        self.color = ORANGE
        self.speed = speed      # subclass will replace this value
        self.health = 25 # subclass will replace this value
        self.health_max = self.health

    def draw(self, screen):
        if self.health > self.health_max // 2:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        else:
            pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))

    def get_center(self):
        return (self.x + self.size//2, self.y + self.size//2)

    def move_towards_player(self, player):
        dx = player.get_center()[0] - self.get_center()[0]
        dy = player.get_center()[1] - self.get_center()[1]
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed




