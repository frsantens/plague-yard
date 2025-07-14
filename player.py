import pygame
import random
from constants import *

class Player():
    def __init__(self,x,y):
        # basic properties
        self.x = x
        self.y = y
        self.size = 35 
        self.color = BLUE
        self.font = pygame.font.Font(None, 20)
        self.alive = True
        self.kills = 0
        
        # stats
        self.level = 1
        self.experience = 0
        self.experience_to_next_lvl = 25
        self.max_health = 100
        self.health = self.max_health
        self.speed = 8
        
        # attack_spin
        self.attack = 15
        self.attack_cooldown = 1
        # self.attack_rate = 1
        self.attack_timer = 0
        self.attack_range = 100
        self.is_attacking = False
        self.anim_timer = 0
        self.anim_duration = 0.05
        
        self.stats_to_level = ["attack", "speed", "health", "attack cooldown"]  
        
        # self.defense = 1
        # self.dodge = 0.05

    def draw(self, screen):
        if self.is_attacking:
            pygame.draw.circle(screen, WHITE, self.get_center(), self.attack_range)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        hp_text = self.font.render(f'{self.health}/{self.max_health}', True, BLACK)
        screen.blit(hp_text,(self.x, self.y) )
        
    def get_center(self):
        return (self.x + self.size//2, self.y + self.size//2)

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
        # normalise movement before multiplying with speed
        if dx != 0 or dy != 0:
            magnitude = (dx**2 + dy**2)**0.5
            dx = (dx / magnitude) * self.speed
            dy = (dy / magnitude) * self.speed
        self.x += dx
        self.y += dy
        # player can't leave screen
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))
        
    def in_range(self, enemy):
        player_center = self.get_center()
        # Find closest point on rectangle to circle center
        closest_x = max(enemy.x, min(player_center[0], enemy.x + enemy.size))
        closest_y = max(enemy.y, min(player_center[1], enemy.y + enemy.size))
        dx = player_center[0] - closest_x
        dy = player_center[1] - closest_y
        distance = (dx**2 + dy**2)**0.5
        return distance <= self.attack_range
        
    def attack_spin(self, dt, enemies):
        if self.alive:
            self.attack_timer += dt
            if self.attack_timer >= self.attack_cooldown:
                self.is_attacking = True
                self.anim_timer = 0
                self.attack_timer = 0
                for i in range(len(enemies)-1, -1, -1):
                    if enemies[i].health > 0:
                        if self.in_range(enemies[i]):
                            enemies[i].health -= self.attack
                    if enemies[i].health <= 0:
                        enemies.pop(i)
                        self.experience += enemies[i].experience
                        self.kills += 1
                        self.level_up()
            if self.is_attacking:
                self.anim_timer += dt
                if self.anim_timer >= self.anim_duration:
                    self.is_attacking = False
                    
    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.exp_next_lvl:
            self.level_up()

    def level_up(self):
        if self.experience >= self.experience_to_next_lvl:
            self.level += 1
            self.experience = 0
            self.experience_to_next_lvl = int(self.experience_to_next_lvl * 1.5)
            print(f"Level up! You are now level {self.level}.")
            self.upgrade_stat(random.choice(self.stats_to_level))

    def upgrade_stat(self, stat):
        if stat == "attack":
            self.attack += 5
        elif stat == "speed":
            self.speed += 1
        elif stat == "health":
            self.max_health += 20
        elif stat == "attack cooldown":
            self.attack_cooldown *= 0.75
        self.health = self.max_health
        print(f"Upgraded {stat}!")

        self.stats_to_level = ["attack", "speed", "health", "attack cooldown"]  
