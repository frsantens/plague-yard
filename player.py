import pygame
import pygame.gfxdraw
import random
from constants import *

class Player():
    def __init__(self,x,y):
        # basic properties
        self.x = x
        self.y = y
        self.color = PLAYER_COLOR
        self.color_alpha = (*self.color, 10)
        self.hp_font = pygame.font.Font(None, 20)
        self.stats_font = pygame.font.Font(None, 25)
        self.alive = True
        self.is_level_up = False
        self.size = SIZE 
        
        # stats
        self.kills = 0
        self.level = 1
        self.experience = 0
        self.experience_to_next_lvl = EXP_REQ
        self.max_health = HEALTH
        self.health = self.max_health
        self.speed = SPEED
        self.attack = ATTACK
        self.attack_cooldown = ATTACK_COOLDOWN
        
        self.stat_string = ""
        self.hp_text = self.hp_font.render(f'{self.health}', True, BLACK)
        self.level_up_text = self.stats_font.render(f"Level up! level {self.level}, upgraded {self.stat_string}", True, WHITE)
        self.level_up_text_duration = 2
        self.level_up_text_timer = 0
        
        # self.attack_rate = 1
        self.attack_timer = 0
        self.attack_range = ATTACK_RANGE
        self.is_attacking = False
        self.anim_timer = 0
        self.anim_duration = 0.05
        # Create transparent surface for the circle
        self.attack_aoe_surface = pygame.Surface((self.attack_range * 2 + 10, self.attack_range * 2 + 10), pygame.SRCALPHA)
        self.attack_aoe_surface_center = (self.attack_range + 5, self.attack_range + 5)
        
        self.stats_to_level = ["attack", "speed", "health", "attack cooldown"]  
        self.stat_string = ""
        # self.defense = 1
        # self.dodge = 0.05

    def draw(self, screen):
        self.attack_aoe_surface.fill((0,0,0,0)) #clear attack range surface
        pygame.draw.circle(self.attack_aoe_surface, self.color_alpha, self.attack_aoe_surface_center, self.attack_range)
        if self.is_attacking:
            pygame.draw.circle(screen, GREY, self.get_center(), self.attack_range)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
    

        # to position the surface so its center aligns with player
        center = self.get_center()
        x = center[0]
        y = center[1]
        screen.blit(self.attack_aoe_surface, (x - self.attack_range - 5, y - self.attack_range - 5))
        screen.blit(self.hp_text,(self.x, self.y) )
        self.draw_stats_text(screen)
        
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
        
    def attack_area(self, dt, enemies):
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
                        self.experience += enemies[i].experience
                        self.kills += 1
                        self.level_up()
                        enemies.pop(i)
            if self.is_attacking:
                self.anim_timer += dt
                if self.anim_timer >= self.anim_duration:
                    self.is_attacking = False
                    
    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.exp_next_lvl:
            self.level_up(self.level_up_text_duration)

    def level_up(self):
        if self.experience >= self.experience_to_next_lvl:
            self.is_level_up = True
            self.level += 1
            self.experience = 0
            self.experience_to_next_lvl = int(self.experience_to_next_lvl * EXP_REQ_SCALE)
            print(f"Level up! You are now level {self.level}.")
            self.upgrade_stat(random.choice(self.stats_to_level))
            self.level_up_text_timer = 0
            self.level_up_text = self.stats_font.render(f"Level up! level {self.level}, upgraded {self.stat_string}", True, WHITE)


    def upgrade_stat(self, stat):
        if stat == "attack":
            self.attack += 5
            self.stat_string = "attack"
        elif stat == "speed":
            self.speed += 1
            self.stat_string = "speed"
        elif stat == "health":
            self.max_health += 20
            self.stat_string = "health"
        elif stat == "attack cooldown":
            self.attack_cooldown *= 0.75
            self.stat_string = "attack cooldown"
        self.health = self.max_health
        print(f"Upgraded {stat}!")
        self.stats_to_level = ["attack", "speed", "health", "attack cooldown"]
    
    def update_health_text(self):
        self.hp_text = self.hp_font.render(f'{self.health}', True, BLACK)
        
    def draw_stats_text(self, screen):
        stats_text = []
        stats_text.append(f"level             : {self.level}")
        stats_text.append(f"attack           : {self.attack}")
        stats_text.append(f"speed           : {self.speed}")
        stats_text.append(f"max health  : {self.max_health}")
        stats_text.append(f"cooldown     : {self.attack_cooldown:.2f}")
        offset = 0
        for text in stats_text:
            screen.blit(self.stats_font.render(text, True, WHITE), (10, 70 + offset))
            offset += 20

