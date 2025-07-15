import pygame
from constants import *
from player import Player
from enemy_spawner import EnemySpawner

    

def main():
    # pygame setup
    pygame.init()
    pygame.display.set_caption('Plague yard v1.01')
    game_state = 1 # 0 = game over, 1 = playing, 2 = pause
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 25)
    font_m = pygame.font.Font(None, 35)
    font_l = pygame.font.Font(None, 50)
    font_xl = pygame.font.Font(None, 100)
    clock = pygame.time.Clock()
    running = True

    player = Player(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
    spawner = EnemySpawner(player)
    enemies = []
    
    # Track survival time
    start_time = pygame.time.get_ticks()
    survival_time = 0
    game_over_recorded = False  # Flag to record survival time only once
    
    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and game_state == 0:
                if event.key == pygame.K_SPACE:
                    game_state = 1
                    player = Player(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
                    spawner = EnemySpawner(player)
                    enemies = []
                    start_time = pygame.time.get_ticks()  # Reset timer on restart
                    game_over_recorded = False  # Reset flag on restart
                
        fps_text = font.render(f"FPS: {clock.get_fps():.1f}", True, WHITE)
        enemy_counter_text = font.render(f'enemies : {len(enemies)}', True, WHITE)
        player_lvl_text = font.render(
            f'lvl : {player.level}  exp : {player.experience}/{player.experience_to_next_lvl}   kills : {player.kills} ', True, WHITE
            )
        game_over_text = font_xl.render('GAME OVER!!', True, WHITE, ORANGE)
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        restart_text = font_l.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect()
        restart_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)

 
        screen.fill(BLACK)

        if not player.alive and not game_over_recorded:
            game_state = 0
            survival_time = (pygame.time.get_ticks() - start_time) / 1000.0  # Convert to seconds
            game_over_recorded = True  # this way we only store survival_time once, otherwise it keeps running at game over
            
        if game_state == 1:
            player.move()
            for enemy in enemies:
                enemy.move_towards_player(player)
                enemy.attack_player(dt, player)
            player.attack_area(dt, enemies)
            spawner.update(dt,enemies)

            player.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)
            if player.is_level_up and player.level_up_text_timer <= player.level_up_text_duration:
                player.level_up_txt_rect = player.level_up_text.get_rect()
                player.level_up_txt_rect.center = (player.get_center()[0], player.get_center()[1] - 30)
                screen.blit(player.level_up_text,(player.level_up_txt_rect))
                player.level_up_text_timer += dt
                
            
            screen.blit(fps_text, (10, 10))
            screen.blit(enemy_counter_text, (10, 30))
            screen.blit(player_lvl_text, (10, 50))
        
        else: 
            minutes = int(survival_time // 60)
            seconds = int(survival_time % 60)
            stats_lines = [
                f"Time Survived: {minutes}:{seconds:02d}",
                f"Enemies Killed: {player.kills}",
                f"Level Reached: {player.level}",
                f"Final Attack: {player.attack}",
                f"Final Speed: {player.speed}",
                f"Final Health: {player.max_health}",
                f"Final Cooldown: {player.attack_cooldown:.2f}s"
            ]
            
            screen.blit(game_over_text, game_over_text_rect)
            screen.blit(restart_text, restart_rect)
            
            stats_start_y = SCREEN_HEIGHT // 2 - 250
            i = 0
            for stat_line in stats_lines:
                stat_text = font_m.render(stat_line, True, WHITE)
                stat_rect = stat_text.get_rect()
                stat_rect.center = (SCREEN_WIDTH // 2, stats_start_y + i * 30)
                screen.blit(stat_text, stat_rect)
                i += 1
            
            
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60

    pygame.quit()
if __name__ == "__main__":

    main()