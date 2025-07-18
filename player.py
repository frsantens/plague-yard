import pygame as pg
import random
from constants import *

class Player():
    # Class variables - same for all players
    size = SIZE
    stats_to_level = ["atk", "speed", "hp", "atk cd", "def", "dodge", "shock cd"]
    level_up_txt_duration = 1.5
    anim_duration = 0.1
    shock_duration = 0.2
    shock_cd = SHOCK_COOLDOWN
    
    def __init__(self, x, y):
        # basic properties
        self.x = x
        self.y = y
        self.color = PLAYER_COLOR
        self.color_alpha = (*self.color, 10)
        self.hp_font = pg.font.Font(None, 20)
        self.stats_font = pg.font.Font(None, 20)
        self.lvl_up_font = pg.font.Font(None, 35)
        self.osd_font = pg.font.SysFont('courier', 18)
        self.alive = True
        self.is_level_up = False
        
        # initial stats
        self.kills = 0
        self.level = 1
        self.experience = 0
        self.experience_to_next_lvl = EXP_REQ
        self.max_hp = HEALTH
        self.hp = self.max_hp
        self.speed = SPEED
        # damage reduction = (1 - (1/player.defense) ) * 100
        self.defense = 1  
        # dodge chance = player.dodge / (2 * player.dodge + 100) 
        self.dodge = 5 
        
        self.atk = ATTACK
        self.atk_cd = ATTACK_COOLDOWN
        self.atk_timer = 0
        self.atk_range = ATTACK_RANGE
        self.shock_range = SHOCK_RANGE
        self.is_atking = False
        self.anim_timer = 0
        self.atk_aoe_surface = pg.Surface(
            (self.atk_range * 2 + 10, self.atk_range * 2 + 10), pg.SRCALPHA
            )
        self.atk_aoe_surface_center = (self.atk_range + 5, self.atk_range + 5)
        
        self.shock_timer = 0
        self.is_shocking = False
        self.shock_lines = []
        self.shock_effect_timer = 0
        self.shock_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
        
        self.stat_string = ""
        
        self.hp_text = self.hp_font.render(f'{self.hp:.0f}', True, WHITE)
        self.level_up_txt = self.lvl_up_font.render(
            f"Level up! level {self.level}, upgraded {self.stat_string}", 
            True, WHITE
            )
        self.level_up_txt_timer = 0
        
    def draw(self, scrn):
        center = self.get_center()
        self._update_player_color()
        self._draw_attack_range(scrn, center)
        self._draw_player_body(scrn)
        if self.is_atking:
            self._draw_attack_animation(scrn, center)
        if self.is_shocking:
            self._draw_shock_effect(scrn)        
        self._draw_hp_text(scrn, center)
    
    def _update_player_color(self):
        # this fixes color value error 
        current_hp = max(0, self.hp)
        hp_percentage = current_hp / self.max_hp
        
        if hp_percentage < 1.0:
            fade_factor = 1.0 - hp_percentage
            original_color = PLAYER_COLOR
            self.color = (
                int(original_color[0] * (1 - fade_factor)),
                int(original_color[1] * (1 - fade_factor)),
                int(original_color[2] * (1 - fade_factor))
                )
            # adjust alpha aoe indicator
            alpha_intensity = int(10 + (15 * fade_factor))  # 10 to 25
            self.color_alpha = (*self.color, alpha_intensity)
        else:
            self.color = PLAYER_COLOR
            self.color_alpha = (*PLAYER_COLOR, 10)
    
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
    
    def _draw_player_body(self, scrn):
        pg.draw.rect(scrn, self.color, (self.x, self.y, self.size, self.size))
    
    def _draw_attack_animation(self, scrn, center):
        attack_progress = self.anim_timer / self.anim_duration
        attack_alpha = int(255 * (1 - attack_progress))
        attack_color = (*GREEN, attack_alpha)
        attack_surface = pg.Surface((self.atk_range * 2, self.atk_range * 2), pg.SRCALPHA)
        pg.draw.circle(attack_surface, attack_color, (self.atk_range, self.atk_range), self.atk_range)
        scrn.blit(attack_surface, (center[0] - self.atk_range, center[1] - self.atk_range))
    
    def _draw_shock_effect(self, scrn):
        alpha_progress = 1.0 - (self.shock_effect_timer / self.shock_duration)
        alpha = int(255 * alpha_progress)
        self.shock_surface.fill((0, 0, 0, 0))
        white_with_alpha = (*WHITE, alpha)
        
        for line in self.shock_lines:
            # each line contains (source_entity, target_entity, thickness)
            source_entity, target_entity, thickness = line
            if source_entity == "player":
                start_pos = self.get_center()
            else:
                start_pos = source_entity.get_center()
            end_pos = target_entity.get_center()
            pg.draw.line(self.shock_surface, white_with_alpha, start_pos, end_pos, thickness)
        
        scrn.blit(self.shock_surface, (0, 0))
    
    def _draw_hp_text(self, scrn, center):
        hp_text_rect = self.hp_text.get_rect()
        hp_text_rect.center = center
        scrn.blit(self.hp_text, hp_text_rect)
        
    def get_center(self):
        return (self.x + self.size//2, self.y + self.size//2)

    def move(self):
        keys = pg.key.get_pressed()
        
        dx = 0
        dy = 0
        if any(keys[k] for k in K_LEFT):
            dx -= 1
        if any(keys[k] for k in K_RIGHT):
            dx += 1
        if any(keys[k] for k in K_UP):
            dy -= 1
        if any(keys[k] for k in K_DOWN):
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
        
    def in_range(self, enemy, attack_type="normal"):
        # Select the appropriate range based on attack type
        if attack_type == "shock":
            range_to_use = self.shock_range
        else:
            range_to_use = self.atk_range
        if enemy.enemy_type != "Boss":
            player_center = self.get_center()
            # find closest point on enemy to player center
            closest_x = max(
                enemy.x, min(player_center[0], enemy.x + enemy.size)
                )
            closest_y = max(
                enemy.y, min(player_center[1], enemy.y + enemy.size)
                )
            dx = player_center[0] - closest_x
            dy = player_center[1] - closest_y
            distance = (dx**2 + dy**2)**0.5
            return distance <= range_to_use
        else:
            player_center = self.get_center()
            boss_center = enemy.get_center()
            dx = player_center[0] - boss_center[0]
            dy = player_center[1] - boss_center[1]
            distance = (dx**2 + dy**2)**0.5
            return distance <= (range_to_use + enemy.size)
        
    def atk_area(self, dt, enemies):
        if self.alive:
            self.atk_timer += dt
            if self.atk_timer >= self.atk_cd:
                self.is_atking = True
                self.anim_timer = 0
                self.atk_timer = 0
                for enemy in enemies:
                    if enemy.hp > 0 and not enemy.is_dying:
                        if self.in_range(enemy):
                            enemy.hp -= self.atk
                            enemy.update_hp_text()
                            if enemy.hp <= 0:
                                enemy.start_death_animation()
                                self.gain_experience(enemy.experience)
                                self.kills += 1
            if self.is_atking:
                self.anim_timer += dt
                if self.anim_timer >= self.anim_duration:
                    self.is_atking = False
                    
        for i in range(len(enemies)-1, -1, -1):
            if enemies[i].update(dt):  # true when death animation is complete
                enemies.pop(i)
                    
    def atk_shock(self, dt, enemies):
        # fire two shocks to the two nearest enemies with chaining effect
        if self.alive:
            self.shock_timer += dt
            
            if self.is_shocking:
                self.shock_effect_timer += dt
                if self.shock_effect_timer >= self.shock_duration:
                    self.is_shocking = False
                    self.shock_lines = []
                    self.shock_effect_timer = 0
            
            if self.shock_timer >= self.shock_cd and len(enemies) > 0:
                self.is_shocking = True
                self.shock_lines = []
                self.shock_timer = 0
                self.shock_effect_timer = 0
                
                enemy_distances = []
                for i, enemy in enumerate(enemies):
                    if enemy.hp > 0 and not enemy.is_dying and self.in_range(enemy, "shock"):
                        player_center = self.get_center()
                        enemy_center = enemy.get_center()
                        dx = player_center[0] - enemy_center[0]
                        dy = player_center[1] - enemy_center[1]
                        distance = (dx**2 + dy**2)**0.5
                        enemy_distances.append((distance, i, enemy))
                
                # sort by distance and get the two nearest
                enemy_distances.sort(key=lambda x: x[0])
                first_wave_targets = enemy_distances[:2]
                hit_enemies = set()
                # first wave: player attacks two nearest enemies
                for distance, i, enemy in first_wave_targets:
                    if enemy.hp > 0 and not enemy.is_dying:
                        self.shock_lines.append(("player", enemy, 2))
                        enemy.hp -= self.atk // 2
                        enemy.update_hp_text()
                        hit_enemies.add(i)
                        # Check if enemy dies and start death animation
                        if enemy.hp <= 0:
                            enemy.start_death_animation()
                            self.gain_experience(enemy.experience)
                            self.kills += 1
                        
                        # Second wave: Each hit enemy attacks their two nearest enemies
                        self._chain_shock(enemy, enemies, hit_enemies, self.atk // 4)  # half shock damage
    
    def _chain_shock(self, source_enemy, all_enemies, hit_enemies, damage):
        # find all enemies and their distances from the source enemy
        enemy_distances = []
        source_center = source_enemy.get_center()
        
        for i, enemy in enumerate(all_enemies):
            if enemy.hp > 0 and not enemy.is_dying and i not in hit_enemies:
                enemy_center = enemy.get_center()
                dx = source_center[0] - enemy_center[0]
                dy = source_center[1] - enemy_center[1]
                distance = (dx**2 + dy**2)**0.5
                enemy_distances.append((distance, i, enemy))
        
        enemy_distances.sort(key=lambda x: x[0])
        second_wave_targets = enemy_distances[:2]
        
        # attack the two nearest enemies
        for distance, i, enemy in second_wave_targets:
            if enemy.hp > 0 and not enemy.is_dying:
                self.shock_lines.append((source_enemy, enemy, 1))
                enemy.hp -= damage
                enemy.update_hp_text()
                hit_enemies.add(i)
                
                # Check if enemy dies and start death animation
                if enemy.hp <= 0:
                    enemy.start_death_animation()
                    self.gain_experience(enemy.experience)
                    self.kills += 1
                    
    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.experience_to_next_lvl:
            self.level_up()

    def level_up(self):
        self.is_level_up = True
        self.level += 1
        self.experience -= self.experience_to_next_lvl
        self.experience_to_next_lvl = int(
            self.experience_to_next_lvl * EXP_REQ_MULT
            )
        print(f"Level up! You are now level {self.level}.")
        # choices() returns a list with 1 string
        # ["atk", "speed", "hp", "atk cd", "def", "dodge", "shock cd"]
        self.stat_string = random.choices(
            self.stats_to_level, weights=[3, 2, 3, 2, 8, 9, 8]
            )[0]
        self.upgrade_stat(self.stat_string)
        self.update_hp_text()
        self.level_up_txt_timer = 0
        self.level_up_txt = self.lvl_up_font.render(
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
            self.atk_cd *= 0.9
            self.stat_string = "atk cd"
        elif stat == "def":
            self.defense += 0.1
            self.stat_string = "def"
        elif stat == "dodge":
            self.dodge += 5
        elif stat == "shock cd":
            self.shock_cd *= 0.9
        self.hp = self.max_hp
        print(f"Upgraded {stat}!")
    
    def update_hp_text(self):
        self.hp_text = self.hp_font.render(f'{self.hp}', True, WHITE)
        
    def draw_stats_text(self, scrn):
        damage_reduction = (1 - (1 / self.defense)) * 100
        dodge_chance = self.dodge / (2 * self.dodge + 100) * 100
        stats_text = []
        stats_text.append(f"level   : {self.level}")
        stats_text.append(f"attack  : {self.atk}")
        stats_text.append(f"hp      : {int(self.hp)}/{self.max_hp}")
        stats_text.append(f"defense  : {damage_reduction:.1f}%")
        stats_text.append(f"dodge    : {dodge_chance:.1f}%")
        
        column_split = 3
        for i, text in enumerate(stats_text):
            if i < column_split:
                x_pos = 10
                y_pos = 46 + i * 18
            else: 
                x_pos = 230
                y_pos = 46 + (i - column_split) * 18
            
            scrn.blit(
                self.osd_font.render(text, True, WHITE), (x_pos, y_pos)
                )

