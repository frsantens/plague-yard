import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.color = (0, 255, 0)
        self.speed = 5
        self.attack = 10
        self.dodge = 0.1  # 10% chance to dodge
        self.defense = 5
        self.critical_chance = 0.2  # 20% chance for critical hit
        self.sword_cooldown = 0
        self.fireball_cooldown = 0
        self.level = 1
        self.experience = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, keys):
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

    def attack_enemy(self, enemy):
        if self.sword_cooldown <= 0:
            # Sword attack logic
            pass

    def shoot_fireball(self, enemies):
        if self.fireball_cooldown <= 0:
            # Fireball tracking logic
            pass

    def level_up(self):
        self.level += 1
        self.experience = 0
        # Upgrade stats logic
        pass
