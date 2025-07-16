import pygame as pg
import random
from constants import *

class Player():
    def __init__(self,x,y):
        # basic properties
        self.x = x
        self.y = y
        self.color = PLAYER_COLOR
        self.color_alpha = (*self.color, 10)
        self.hp_font = pg.font.Font(None, 20)
        self.stats_font = pg.font.Font(None, 25)
        self.alive = True
        self.is_level_up = False
        self.size = SIZE 
        
        # stats
        self.kills = 0
        self.level = 1
        self.experience = 0
        self.experience_to_next_lvl = EXP_REQ
        self.max_hp = HEALTH
        self.hp = self.max_hp
        self.speed = SPEED
        self.atk = ATTACK
        self.atk_cd = ATTACK_COOLDOWN
        
        self.stat_string = ""
        self.hp_text = self.hp_font.render(f'{self.hp}', True, BLACK)
        self.level_up_text = self.stats_font.render(
            f"Level up! level {self.level}, upgraded {self.stat_string}", 
            True, WHITE
            )
        self.level_up_text_duration = 2
        self.level_up_text_timer = 0
        
        # self.atk_rate = 1
        self.atk_timer = 0
        self.atk_range = ATTACK_RANGE
        self.is_atking = False
        self.anim_timer = 0
        self.anim_duration = 0.05
        # Create transparent surface for the circle
        self.atk_aoe_surface = pg.Surface(
            (self.atk_range * 2 + 10, self.atk_range * 2 + 10), pg.SRCALPHA
            )
        self.atk_aoe_surface_center = (self.atk_range + 5, self.atk_range + 5)
        
        self.stats_to_level = ["atk", "speed", "hp", "atk cd"]  
        self.stat_string = ""
        # self.defense = 1
        # self.dodge = 0.05

    def draw(self, scrn):
        self.atk_aoe_surface.fill((0,0,0,0)) #clear atk range surface
        pg.draw.circle(
            self.atk_aoe_surface, self.color_alpha, 
            self.atk_aoe_surface_center, self.atk_range
            )
        if self.is_atking:
            pg.draw.circle(scrn, GREEN, self.get_center(), self.atk_range)
        pg.draw.rect(scrn, self.color, (self.x, self.y, self.size, self.size))
    

        # to position the surface so its center aligns with player
        center = self.get_center()
        x = center[0]
        y = center[1]
        scrn.blit(
            self.atk_aoe_surface, 
            (x - self.atk_range - 5, y - self.atk_range - 5)
            )
        scrn.blit(self.hp_text,(self.x, self.y) )
        
    def get_center(self):
        return (self.x + self.size//2, self.y + self.size//2)

    def move(self):
        keys = pg.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pg.K_LEFT]:
            dx -= 1
        if keys[pg.K_RIGHT]:
            dx += 1
        if keys[pg.K_UP]:
            dy -= 1
        if keys[pg.K_DOWN]:
            dy += 1
        # normalise movement before multiplying with speed
        if dx != 0 or dy != 0:
            magnitude = (dx**2 + dy**2)**0.5
            dx = (dx / magnitude) * self.speed
            dy = (dy / magnitude) * self.speed
        self.x += dx
        self.y += dy
        # player can't leave scrn
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))
        
    def in_range(self, enemy):
        if enemy.enemy_type != "Boss":
            player_center = self.get_center()
            # Find closest point on rectangle to circle center
            closest_x = max(
                enemy.x, min(player_center[0], enemy.x + enemy.size)
                )
            closest_y = max(
                enemy.y, min(player_center[1], enemy.y + enemy.size)
                )
            dx = player_center[0] - closest_x
            dy = player_center[1] - closest_y
            distance = (dx**2 + dy**2)**0.5
            return distance <= self.atk_range
        else:
            player_center = self.get_center()
            boss_center = enemy.get_center()
            dx = player_center[0] - boss_center[0]
            dy = player_center[1] - boss_center[1]
            distance = (dx**2 + dy**2)**0.5
            return distance <= (self.atk_range + enemy.size)
        
    def atk_area(self, dt, enemies):
        if self.alive:
            self.atk_timer += dt
            if self.atk_timer >= self.atk_cd:
                self.is_atking = True
                self.anim_timer = 0
                self.atk_timer = 0
                for i in range(len(enemies)-1, -1, -1):
                    if enemies[i].hp > 0:
                        if self.in_range(enemies[i]):
                            enemies[i].hp -= self.atk
                            enemies[i].update_hp_text()
                    if enemies[i].hp <= 0:
                        self.experience += enemies[i].experience
                        self.kills += 1
                        self.level_up()
                        enemies.pop(i)
            if self.is_atking:
                self.anim_timer += dt
                if self.anim_timer >= self.anim_duration:
                    self.is_atking = False
                    
    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.exp_next_lvl:
            self.level_up(self.level_up_text_duration)

    def level_up(self):
        if self.experience >= self.experience_to_next_lvl:
            self.is_level_up = True
            self.level += 1
            self.experience = 0
            self.experience_to_next_lvl = int(
                self.experience_to_next_lvl * EXP_REQ_MULT
                )
            print(f"Level up! You are now level {self.level}.")
            # choices() returns a list with 1 string, so acces index 0
            self.stat_string = random.choices(
                self.stats_to_level, weights=(0.2,0.2,0.3,0.3)
                )[0]
            self.upgrade_stat(self.stat_string)
            self.update_hp_text()
            self.level_up_text_timer = 0
            self.level_up_text = self.stats_font.render(
                f"Level up! level {self.level}, upgraded {self.stat_string}", 
                True, WHITE
                )


    def upgrade_stat(self, stat):
        if stat == "atk":
            self.atk += 5
            self.stat_string = "atk"
        elif stat == "speed":
            self.speed += 1
            self.stat_string = "speed"
        elif stat == "hp":
            self.max_hp += 20
            self.stat_string = "hp"
        elif stat == "atk cd":
            self.atk_cd *= 0.75
            self.stat_string = "atk cd"
        self.hp = self.max_hp
        print(f"Upgraded {stat}!")
        self.stats_to_level = ["atk", "speed", "hp", "atk cd"]
    
    def update_hp_text(self):
        self.hp_text = self.hp_font.render(f'{self.hp}', True, BLACK)
        
    def draw_stats_text(self, scrn):
        stats_text = []
        stats_text.append(f"level             : {self.level}")
        stats_text.append(f"attack           : {self.atk}")
        stats_text.append(f"speed           : {self.speed}")
        stats_text.append(f"max health  : {self.max_hp}")
        stats_text.append(f"cooldown     : {self.atk_cd:.2f}")
        offset = 0
        for text in stats_text:
            scrn.blit(
                self.stats_font.render(text, True, WHITE), (10, 70 + offset)
                )
            offset += 20

