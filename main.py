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
    font = pg.font.SysFont('courier', 18)
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
    pause_start_time = 0
    total_pause_time = 0
    game_over_recorded = False  # record survival time only once
    pause_key_pressed = False
    
    while running:
        dt = clock.tick(60) / 1000
        
        # check for pause with toggle
        keys = pg.key.get_pressed()
        if keys[pg.K_f] and not pause_key_pressed:
            pause_key_pressed = True
            if game_state == 1:
                print("Pausing game") 
                game_state = 2
                pause_start_time = pg.time.get_ticks()  # record when pause started
            elif game_state == 2:
                print("Unpausing game") 
                game_state = 1
                total_pause_time += pg.time.get_ticks() - pause_start_time
        elif not keys[pg.K_f]:
            pause_key_pressed = False
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and game_state == 0:
                if event.key == pg.K_SPACE:
                    game_state = 1
                    player = Player(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
                    spawner = EnemySpawner(player)
                    enemies = []
                    start_time = pg.time.get_ticks()  # reset timer on restart
                    total_pause_time = 0 
                    game_over_recorded = False
        scrn.fill(BLACK)

        if not player.alive and not game_over_recorded:
            game_state = 0
            survival_time = (
                pg.time.get_ticks() - start_time - total_pause_time
                ) / 1000.0
            # store once, otherwise it keeps running at game over
            game_over_recorded = True  
            
        if game_state == 1:
            player.move()
            for enemy in enemies:
                enemy.move_towards_player(player)
                enemy.atk_player(dt, player)
            player.atk_area(dt, enemies)
            player.atk_shock(dt, enemies)
            spawner.update(dt,enemies)
            player.draw(scrn)
            for enemy in enemies:
                enemy.draw(scrn)
            if player.is_level_up:
                if player.level_up_txt_timer <= player.level_up_txt_duration:
                    player.level_up_txt_rect = player.level_up_txt.get_rect()
                    player.level_up_txt_rect.center = (
                        player.get_center()[0], player.get_center()[1] - 30
                        )
                    scrn.blit(player.level_up_txt,(player.level_up_txt_rect))
                    player.level_up_txt_timer += dt
                else: player.is_level_up = False 
            # on screen display of stats
            osd_stats = [
                f'enemies : {len(enemies)}',
                f'kills   : {player.kills}',
                f'lvl     : {player.level}',
                f'exp     : {player.experience}/{player.experience_to_next_lvl}'
            ]
            column_split = len(osd_stats) // 2
            for i, text in enumerate(osd_stats):
                if i < column_split:
                    x_pos = 10
                    y_pos = 10 + i * 18
                else:
                    x_pos = 230
                    y_pos = 10 + (i - column_split) * 18
                scrn.blit(font.render(text, True, WHITE), (x_pos, y_pos))
            player.draw_stats_text(scrn)
        elif game_state == 2:
            # Use the survival time at the moment pause started (frozen)
            current_survival_time = (
                pause_start_time - start_time - total_pause_time
                ) / 1000.0
            minutes = int(current_survival_time // 60)
            seconds = int(current_survival_time % 60)
            pause_text = font_xl.render('PAUSED', True, WHITE, ORANGE)
            pause_text_rect = pause_text.get_rect()
            pause_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            restart_text = font_l.render("Press F to unpause", True, WHITE)
            restart_rect = restart_text.get_rect()
            restart_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            damage_reduction = (1 - (1 / player.defense)) * 100
            dodge_chance = player.dodge / (2 * player.dodge + 100) * 100
            stats_lines = [
                f"Time Survived: {minutes}:{seconds:02d}",
                f"Enemies Killed: {player.kills}",
                f"Level Reached: {player.level}",
                f"Final Attack: {player.atk}",
                f"Final Cooldown: {player.atk_cd:.2f}s",
                f"Final Speed: {player.speed}",
                f"Final Health: {player.max_hp}",
                f'Final Defense: {damage_reduction:.1f}%',
                f'Final Dodge: {dodge_chance:.1f}%'
            ]
            scrn.blit(pause_text, pause_text_rect)
            scrn.blit(restart_text, restart_rect)
            offset = 30
            stats_start_y = SCREEN_HEIGHT // 2 - (len(stats_lines)+1.2)*(offset) 
            i = 0
            for stat_line in stats_lines: 
                stat_text = font_m.render(stat_line, True, WHITE)
                stat_rect = stat_text.get_rect()
                stat_rect.center = (SCREEN_WIDTH // 2, stats_start_y + i * offset)
                scrn.blit(stat_text, stat_rect)
                i += 1
        else: 
            minutes = int(survival_time // 60)
            seconds = int(survival_time % 60)
            game_over_text = font_xl.render('GAME OVER!!', True, WHITE, ORANGE)
            game_over_text_rect = game_over_text.get_rect()
            game_over_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            restart_text = font_l.render("Press SPACE to restart", True, WHITE)
            restart_rect = restart_text.get_rect()
            restart_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            damage_reduction = (1 - (1 / player.defense)) * 100
            dodge_chance = player.dodge / (2 * player.dodge + 100) * 100
            stats_lines = [
                f"Time Survived: {minutes}:{seconds:02d}",
                f"Enemies Killed: {player.kills}",
                f"Level Reached: {player.level}",
                f"Final Attack: {player.atk}",
                f"Final Cooldown: {player.atk_cd:.2f}s",
                f"Final Speed: {player.speed}",
                f"Final Health: {player.max_hp}",
                f'Final Defense: {damage_reduction:.1f}%',
                f'Final Dodge: {dodge_chance:.1f}%'
            ]
            scrn.blit(game_over_text, game_over_text_rect)
            scrn.blit(restart_text, restart_rect)
            
            offset = 30
            stats_start_y = SCREEN_HEIGHT // 2 - (len(stats_lines)+1.2)*(offset) 
            i = 0
            for stat_line in stats_lines: 
                stat_text = font_m.render(stat_line, True, WHITE)
                stat_rect = stat_text.get_rect()
                stat_rect.center = (SCREEN_WIDTH // 2, stats_start_y + i * offset)
                scrn.blit(stat_text, stat_rect)
                i += 1
            
            
        pg.display.flip()

    pg.quit()
if __name__ == "__main__":

    main()