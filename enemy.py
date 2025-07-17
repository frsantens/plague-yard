import pygame as pg
import random
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
        self.death_color = GREY
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
        
        self.is_dying = False
        self.death_timer = 0
        self.death_duration = 0.2
        self.original_color = self.color

    def draw(self, scrn):
        center = self.get_center()
        self._update_colors()
        self._draw_enemy_body(scrn, center)
        if not self.is_dying:
            self._draw_attack_range(scrn, center)
        if self.is_atking:
            self._draw_attack_animation(scrn, center)
        if not self.is_dying:
            self._draw_hp_text(scrn, center)
    
    def _update_colors(self):
        if self.is_dying:
            death_progress = self.death_timer / self.death_duration
            alpha = int(255 * (1 - death_progress))
            self.death_color = (*self.color, alpha)
        else:
            hp_percentage = self.hp / self.hp_max            
            if hp_percentage < 1.0:
                fade_factor = 1.0 - hp_percentage
                original_color = self.original_color
                self.color = (
                    int(original_color[0] * (1 - fade_factor) + RED[0] * fade_factor),
                    int(original_color[1] * (1 - fade_factor) + RED[1] * fade_factor),
                    int(original_color[2] * (1 - fade_factor) + RED[2] * fade_factor)
                    )
                # increase alpha intensity as HP decreases
                alpha_intensity = int(8 + (12 * fade_factor))  # 8 to 20
                self.color_alpha = (*self.color, alpha_intensity)
            else:
                # full HP - use original color
                self.color = self.original_color
                self.color_alpha = (*self.color, 8)
            
            self.death_color = self.color
    
    def _draw_enemy_body(self, scrn, center):
        if self.is_dying:
            if self.enemy_type == "Boss":
                boss_surface = pg.Surface((self.size * 2, self.size * 2), pg.SRCALPHA)
                pg.draw.circle(boss_surface, self.death_color, (self.size, self.size), self.size)
                scrn.blit(boss_surface, (center[0] - self.size, center[1] - self.size))
            else:
                enemy_surface = pg.Surface((self.size, self.size), pg.SRCALPHA)
                pg.draw.rect(enemy_surface, self.death_color, (0, 0, self.size, self.size))
                scrn.blit(enemy_surface, (self.x, self.y))
        else:
            if self.enemy_type == "Boss":
                pg.draw.circle(scrn, BOSS_ORANGE, center, self.size)
            else:
                pg.draw.rect(scrn, self.color, (self.x, self.y, self.size, self.size))
    
    def _draw_attack_range(self, scrn, center):
        self.atk_aoe_surface.fill((0, 0, 0, 0))
        pg.draw.circle(
            self.atk_aoe_surface, self.color_alpha,
            self.atk_aoe_surface_center, self.atk_range
            )
        scrn.blit(
            self.atk_aoe_surface,
            (center[0] - self.atk_range - 5, center[1] - self.atk_range - 5)
            )
    
    def _draw_attack_animation(self, scrn, center):
        if self.anim_duration > 0:
            attack_progress = min(self.anim_timer / self.anim_duration, 1.0)
            attack_alpha = max(0, int(255 * (1 - attack_progress)))
        else:
            attack_alpha = 255
        
        attack_color = (*ULTRARED, attack_alpha)
        attack_surface = pg.Surface((self.atk_range * 2, self.atk_range * 2), pg.SRCALPHA)
        pg.draw.circle(attack_surface, attack_color, (self.atk_range, self.atk_range), self.atk_range)
        scrn.blit(attack_surface, (center[0] - self.atk_range, center[1] - self.atk_range))
    
    def _draw_hp_text(self, scrn, center):
        hp_text_rect = self.hp_text.get_rect()
        hp_text_rect.center = center
        scrn.blit(self.hp_text, hp_text_rect)
        
    def update_hp_text(self):
        self.hp_text = self.hp_font.render(f'{self.hp}', True, BLACK)
        
    def update(self, dt):
        if self.is_dying:
            self.death_timer += dt
            if self.death_timer >= self.death_duration:
                return True  # enemy can be removed
        return False  # still alive or still dying

    def start_death_animation(self):
        self.is_dying = True
        self.death_timer = 0

    def get_center(self):
        return (self.x + self.size//2, self.y + self.size//2)

    def move_towards_player(self, player):
        if self.is_dying:
            return 
        dx = player.get_center()[0] - self.get_center()[0]
        dy = player.get_center()[1] - self.get_center()[1]
        distance = (dx**2 + dy**2)**0.5
        if distance > (player.size + self.size)//2:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def atk_player(self, dt, player):
        if self.is_dying:
            return 
        self.atk_timer += dt
        if self.in_range(player) and self.atk_timer >= self.atk_cd:
            dodge = random.choices(
                [True, False], 
                weights=[player.dodge, 100+player.dodge]
                )[0]
            if not dodge:
                player.hp -= self.atk // player.defense
                if player.hp <= 0:
                    player.alive = False
            else: print(f'dodged {self.atk} damage!')
            player.update_hp_text() 
            self.is_atking = True
            self.anim_timer = 0
            self.atk_timer = 0
        if self.is_atking:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_duration:
                self.is_atking = False

    def in_range(self, player):
        enemy_center = self.get_center()
        # Find closest point on self to player (circle)
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
        self.hp_font = pg.font.Font(None, 30)
        self.hp_text = self.hp_font.render(f'{self.hp}', True, WHITE)
        self.color = BOSS_ORANGE
        # need to create surface per class
        self.atk_aoe_surface = pg.Surface(
            (self.atk_range * 2 + 10, self.atk_range * 2 + 10), pg.SRCALPHA
            )
        self.atk_aoe_surface_center = (self.atk_range + 5, self.atk_range + 5)
        
    def update_hp_text(self):
        self.hp_text = self.hp_font.render(f'{self.hp}', True, WHITE)

