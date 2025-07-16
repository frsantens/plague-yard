import pygame as pg
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, BLACK, WHITE, ORANGE
from player import Player
from enemy_spawner import EnemySpawner

def main():
    # pygame setup
    pg.init()
    pg.display.set_caption('Plague yard v1.01')
    game_state = 1 # 0 = game over, 1 = playing, 2 = pause
    scrn = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pg.font.Font(None, 25)
    font_m = pg.font.Font(None, 35)
    font_l = pg.font.Font(None, 50)
    font_xl = pg.font.Font(None, 100)
    clock = pg.time.Clock()
    running = True

    player = Player(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
    spawner = EnemySpawner(player)
    enemies = []
    
    # Track survival time
    start_time = pg.time.get_ticks()
    survival_time = 0
    game_over_recorded = False  # Flag to record survival time only once
    
    while running:
        dt = clock.tick(60) / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and game_state == 0:
                if event.key == pg.K_SPACE:
                    game_state = 1
                    player = Player(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
                    spawner = EnemySpawner(player)
                    enemies = []
                    start_time = pg.time.get_ticks()  # Reset timer on restart
                    game_over_recorded = False  # Reset flag on restart
                
        fps_text = font.render(f"FPS: {clock.get_fps():.1f}", True, WHITE)
        enemy_counter_text = font.render(
            f'enemies : {len(enemies)}', True, WHITE
            )
        player_lvl_text = font.render(
            f'lvl : {player.level}   '
            f'exp : {player.experience}/{player.experience_to_next_lvl}   '
            f'kills : {player.kills} ', True, WHITE
            )
        game_over_text = font_xl.render('GAME OVER!!', True, WHITE, ORANGE)
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        restart_text = font_l.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect()
        restart_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)

 
        scrn.fill(BLACK)

        if not player.alive and not game_over_recorded:
            game_state = 0
            survival_time = (pg.time.get_ticks() - start_time) / 1000.0
            # store survival_time once, otherwise it keeps running at game over
            game_over_recorded = True  
            
        if game_state == 1:
            player.move()
            for enemy in enemies:
                enemy.move_towards_player(player)
                enemy.atk_player(dt, player)
            player.atk_area(dt, enemies)
            spawner.update(dt,enemies)

            player.draw(scrn)
            for enemy in enemies:
                enemy.draw(scrn)
                
            if player.is_level_up:
                if player.level_up_text_timer <= player.level_up_text_duration:
                    player.level_up_txt_rect = player.level_up_text.get_rect()
                    player.level_up_txt_rect.center = (
                        player.get_center()[0], player.get_center()[1] - 30
                        )
                    scrn.blit(player.level_up_text,(player.level_up_txt_rect))
                    player.level_up_text_timer += dt
                else: player.is_level_up = False
            
                
            player.draw_stats_text(scrn)
            scrn.blit(fps_text, (10, 10))
            scrn.blit(enemy_counter_text, (10, 30))
            scrn.blit(player_lvl_text, (10, 50))
        
        else: 
            minutes = int(survival_time // 60)
            seconds = int(survival_time % 60)
            stats_lines = [
                f"Time Survived: {minutes}:{seconds:02d}",
                f"Enemies Killed: {player.kills}",
                f"Level Reached: {player.level}",
                f"Final Attack: {player.atk}",
                f"Final Speed: {player.speed}",
                f"Final Health: {player.max_hp}",
                f"Final Cooldown: {player.atk_cd:.2f}s"
            ]
            
            scrn.blit(game_over_text, game_over_text_rect)
            scrn.blit(restart_text, restart_rect)
            
            stats_start_y = SCREEN_HEIGHT // 2 - 250
            i = 0
            offset = 30
            for stat_line in stats_lines: 
                stat_text = font_m.render(stat_line, True, WHITE)
                stat_rect = stat_text.get_rect()
                stat_rect.center = (SCREEN_WIDTH // 2, stats_start_y + i*offset)
                scrn.blit(stat_text, stat_rect)
                i += 1
            
            
        pg.display.flip()
        clock.tick(60)  # limits FPS to 60

    pg.quit()
if __name__ == "__main__":

    main()