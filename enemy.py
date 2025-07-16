import pygame as pg
from constants import *


class Enemy():
    def __init__(self, x, y, enemy_type, speed):
        self.x = x
        self.y = y
        self.size = SIZE_STANDARD
        self.center = (self.x + self.size//2, self.y + self.size//2)
        self.enemy_type = enemy_type
        self.hp_font = pg.font.Font(None, 20)
        self.color = ORANGE
        self.color_alpha = (*self.color, 8)
        
        self.speed = speed
        self.hp_max = HEALTH_STANDARD
        self.hp = self.hp_max
        self.experience = EXP_STANDARD
        self.atk = ATTACK_STANDARD
        self.atk_cd = COOLDOWN_STANDARD
        self.atk_range = RANGE_STANDARD
        self.hp_text = self.hp_font.render(f'{self.hp}', True, BLACK)
        # to draw a transp circle I need a new transparent surface
        self.atk_aoe_surface = pg.Surface(
            (self.atk_range * 2 + 10, self.atk_range * 2 + 10), pg.SRCALPHA
            )
        self.atk_aoe_surface_center = (self.atk_range + 5, self.atk_range + 5)
        
        self.is_atking = False
        self.atk_timer = 0
        self.anim_timer = 0
        self.anim_duration = 0.05

    def draw(self, scrn):
        if self.is_atking:
            pg.draw.circle(scrn, ULTRARED, self.get_center(), self.atk_range)
        if self.hp <= self.hp_max // 2:
            self.color = RED
            self.color_alpha = (*self.color, 20)
        else:
            self.color_alpha = (*self.color,8)

        self.atk_aoe_surface.fill((0,0,0,0))
        pg.draw.circle(
            self.atk_aoe_surface, self.color_alpha, 
            self.atk_aoe_surface_center, self.atk_range
            )
        if self.enemy_type == "Boss":
            pg.draw.circle(scrn, self.color, self.get_center(), self.size)
        else:
            pg.draw.rect(
                scrn, self.color, (self.x, self.y, self.size, self.size)
                )

        center = self.get_center()
        x = center[0]
        y = center[1]
        # position the surface so its center aligns with player
        scrn.blit(
            self.atk_aoe_surface, 
            (x - self.atk_range - 5, y - self.atk_range - 5)
            )
        scrn.blit(self.hp_text,(self.x, self.y) )
        
    def update_hp_text(self):
        self.hp_text = self.hp_font.render(f'{self.hp}', True, BLACK)

    def get_center(self):
        return (self.x + self.size//2, self.y + self.size//2)

    def move_towards_player(self, player):
        dx = player.get_center()[0] - self.get_center()[0]
        dy = player.get_center()[1] - self.get_center()[1]
        distance = (dx**2 + dy**2)**0.5
        if distance > (player.size + self.size)//2:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def atk_player(self, dt, player):
        self.atk_timer += dt
        if self.in_range(player) and self.atk_timer >= self.atk_cd :
            player.hp -= self.atk
            player.update_hp_text() 
            self.is_atking = True
            self.anim_timer = 0
            self.atk_timer = 0
            if player.hp <= 0:
                player.alive = False
        if self.is_atking:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_duration:
                self.is_atking = False

    def in_range(self, player):
        enemy_center = self.get_center()
        # Find closest point on rectangle to circle center
        closest_x = max(player.x, min(enemy_center[0], player.x + player.size))
        closest_y = max(player.y, min(enemy_center[1], player.y + player.size))
        dx = enemy_center[0] - closest_x
        dy = enemy_center[1] - closest_y
        distance = (dx**2 + dy**2)**0.5
        return distance <= self.atk_range

class StandardEnemy(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x,y,"Standard", speed)
        self.hp_max = HEALTH_STANDARD
        self.hp = self.hp_max
        self.hp_text = self.hp_font.render(f'{self.hp}', True, BLACK)
        # need to create surface per class
        self.atk_aoe_surface = pg.Surface(
            (self.atk_range * 2 + 10, self.atk_range * 2 + 10), pg.SRCALPHA
            )
        self.atk_aoe_surface_center = (self.atk_range + 5, self.atk_range + 5)
        
class SlowStrongEnemy(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x,y,"SlowStrong",speed)
        self.size = SIZE_SLOW_AND_STRONG
        self.speed = speed * SPD_MOD_SLOW_AND_STRONG
        self.hp_max = HEALTH_SLOW_AND_STRONG
        self.hp = self.hp_max
        self.experience = EXP_SLOW_AND_STRONG
        self.atk = ATTACK_SLOW_AND_STRONG
        self.atk_cd = COOLDOWN_SLOW_AND_STRONG
        self.atk_range = RANGE_SLOW_AND_STRONG
        self.hp_text = self.hp_font.render(f'{self.hp}', True, BLACK)
        # need to create surface per class
        self.atk_aoe_surface = pg.Surface(
            (self.atk_range * 2 + 10, self.atk_range * 2 + 10), pg.SRCALPHA
            )
        self.atk_aoe_surface_center = (self.atk_range + 5, self.atk_range + 5)
        
class FastWeakEnemy(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x, y, "FastWeak", speed)
        self.size = SIZE_FAST_AND_WEAK
        self.speed = speed * SPD_MOD_FAST_AND_WEAK
        self.hp_max = HEALTH_FAST_AND_WEAK
        self.hp = self.hp_max
        self.experience = EXP_FAST_AND_WEAK
        self.atk = ATTACK_FAST_AND_WEAK
        self.atk_range = RANGE_FAST_AND_WEAK
        self.atk_cd = COOLDOWN_FAST_AND_WEAK
        self.hp_text = self.hp_font.render(f'{self.hp}', True, BLACK)
        # need to create surface per class
        self.atk_aoe_surface = pg.Surface(
            (self.atk_range * 2 + 10, self.atk_range * 2 + 10), pg.SRCALPHA
            )
        self.atk_aoe_surface_center = (self.atk_range + 5, self.atk_range + 5)
        
        
class BossEnemy(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x, y, "Boss", speed)
        self.hp_max = HEALTH_BOSS
        self.speed = speed * SPD_MOD_BOSS
        self.hp = self.hp_max
        self.size =  SIZE_BOSS
        self.experience = EXP_BOSS
        self.atk = ATTACK_BOSS
        self.atk_range = ATTACK_RANGE_BOSS
        self.atk_cd = COOLDOWN_BOSS
        self.hp_text = self.hp_font.render(f'{self.hp}', True, WHITE)
        self.color = BOSS_ORANGE
        # need to create surface per class
        self.atk_aoe_surface = pg.Surface(
            (self.atk_range * 2 + 10, self.atk_range * 2 + 10), pg.SRCALPHA
            )
        self.atk_aoe_surface_center = (self.atk_range + 5, self.atk_range + 5)
        
        
                

        
        
