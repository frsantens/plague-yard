import pygame
from constants import *


class Enemy():
    def __init__(self, x, y, enemy_type, speed):
        self.x = x
        self.y = y
        self.size = SIZE_STANDARD
        self.center = (self.x + self.size//2, self.y + self.size//2)
        self.font = pygame.font.Font(None, 20)
        self.enemy_type = enemy_type
        self.color = ORANGE
        self.color_alpha = (*self.color, 8)
        
        self.speed = speed
        self.health_max = HEALTH_STANDARD
        self.health = self.health_max
        self.experience = EXP_STANDARD
        self.attack = ATTACK_STANDARD
        self.attack_cooldown = COOLDOWN_STANDARD
        self.attack_range = RANGE_STANDARD
        # to draw a transp circle I need a new transparent surface
        self.attack_aoe_surface = pygame.Surface((self.attack_range * 2 + 10, self.attack_range * 2 + 10), pygame.SRCALPHA)
        self.attack_aoe_surface_center = (self.attack_range + 5, self.attack_range + 5)
        
        self.is_attacking = False
        self.attack_timer = 0
        self.anim_timer = 0
        self.anim_duration = 0.05

    def draw(self, screen):
        if self.is_attacking:
            pygame.draw.circle(screen, ULTRARED, self.get_center(), self.attack_range)
        if self.health <= self.health_max // 2:
            self.color = RED
            self.color_alpha = (*self.color, 20)
        else:
            self.color_alpha = (*self.color,8)

        self.attack_aoe_surface.fill((0,0,0,0))
        pygame.draw.circle(self.attack_aoe_surface, self.color_alpha, self.attack_aoe_surface_center, self.attack_range)
        
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        hp_text = self.font.render(f'{self.health}', True, BLACK)

        center = self.get_center()
        x = center[0]
        y = center[1]
        # position the surface so its center aligns with player
        screen.blit(self.attack_aoe_surface, (x - self.attack_range - 5, y - self.attack_range - 5))
        screen.blit(hp_text,(self.x, self.y) )

    def get_center(self):
        return (self.x + self.size//2, self.y + self.size//2)

    def move_towards_player(self, player):
        dx = player.get_center()[0] - self.get_center()[0]
        dy = player.get_center()[1] - self.get_center()[1]
        distance = (dx**2 + dy**2)**0.5
        if distance > (player.size + self.size)//2:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def attack_player(self, dt, player):
        self.attack_timer += dt
        if self.in_range(player) and self.attack_timer >= self.attack_cooldown :
            player.health -= self.attack
            player.update_health_text() 
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

class SlowStrongEnemy(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x,y,"SlowStrong",speed)
        self.size = SIZE_SLOW_AND_STRONG
        self.speed = speed * SPD_MOD_SLOW_AND_STRONG
        self.health_max = HEALTH_SLOW_AND_STRONG
        self.health = self.health_max
        self.experience = EXP_SLOW_AND_STRONG
        self.attack = ATTACK_SLOW_AND_STRONG
        self.attack_cooldown = COOLDOWN_SLOW_AND_STRONG
        self.attack_range = RANGE_SLOW_AND_STRONG
        
        # need to create surface per class
        self.attack_aoe_surface = pygame.Surface((self.attack_range * 2 + 10, self.attack_range * 2 + 10), pygame.SRCALPHA)
        self.attack_aoe_surface_center = (self.attack_range + 5, self.attack_range + 5)
        
class FastWeakEnemy(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x, y, "FastWeak", speed)
        self.size = SIZE_FAST_AND_WEAK
        self.speed = speed * SPD_MOD_FAST_AND_WEAK
        self.health_max = HEALTH_FAST_AND_WEAK
        self.health = self.health_max
        self.experience = EXP_FAST_AND_WEAK
        self.attack = ATTACK_FAST_AND_WEAK
        self.attack_range = RANGE_FAST_AND_WEAK
        self.attack_cooldown = COOLDOWN_FAST_AND_WEAK
        # need to create surface per class
        self.attack_aoe_surface = pygame.Surface((self.attack_range * 2 + 10, self.attack_range * 2 + 10), pygame.SRCALPHA)
        self.attack_aoe_surface_center = (self.attack_range + 5, self.attack_range + 5)
        
class StandardEnemy(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x,y,"Standard", speed)
        # need to create surface per class
        self.attack_aoe_surface = pygame.Surface((self.attack_range * 2 + 10, self.attack_range * 2 + 10), pygame.SRCALPHA)
        self.attack_aoe_surface_center = (self.attack_range + 5, self.attack_range + 5)
                

        
        
