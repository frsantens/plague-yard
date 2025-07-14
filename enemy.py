import pygame
from constants import *


class Enemy():
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.size = 30
        self.center = (self.x + self.size//2, self.y + self.size//2)
        self.color = ORANGE
        self.font = pygame.font.Font(None, 20)
        
        self.speed = speed      
        self.health_max = 25    # subclass will replace this value
        self.health = self.health_max        
        self.experience = 5
        
        self.attack = 5
        self.attack_cooldown = 1
        # self.attack_rate = 1
        self.attack_timer = 0
        self.attack_range = 40
        self.is_attacking = False
        self.anim_timer = 0
        self.anim_duration = 0.05

    def draw(self, screen):
        if self.is_attacking:
            pygame.draw.circle(screen, ULTRARED, self.get_center(), self.attack_range)
        if self.health > self.health_max // 2:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        else:
            pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))
        hp_text = self.font.render(f'{self.health}/{self.health_max}', True, BLACK)
        screen.blit(hp_text,(self.x, self.y) )

    def get_center(self):
        return (self.x + self.size//2, self.y + self.size//2)

    def move_towards_player(self, player):
        dx = player.get_center()[0] - self.get_center()[0]
        dy = player.get_center()[1] - self.get_center()[1]
        distance = (dx**2 + dy**2)**0.5
        if distance > player.size:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def attack_player(self, dt, player):
        self.attack_timer += dt
        if self.in_range(player) and self.attack_timer >= self.attack_cooldown :
            player.health -= self.attack 
            self.is_attacking = True
            self.anim_timer = 0
            self.attack_timer = 0
            if player.health <= 0:
                player.alive = False
        if self.is_attacking:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_duration:
                self.is_attacking = False

    def in_range(self, player):
        enemy_center = self.get_center()
        # Find closest point on rectangle to circle center
        closest_x = max(player.x, min(enemy_center[0], player.x + player.size))
        closest_y = max(player.y, min(enemy_center[1], player.y + player.size))
        dx = enemy_center[0] - closest_x
        dy = enemy_center[1] - closest_y
        distance = (dx**2 + dy**2)**0.5
        return distance <= self.attack_range



