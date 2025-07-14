# Example file showing a basic pygame "game loop"
import pygame
from constants import *
from player import Player
from enemy_spawner import EnemySpawner


def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None,25)
    clock = pygame.time.Clock()
    running = True

    player = Player(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
    spawner = EnemySpawner(player)
    enemies = []

    while running:
        dt = clock.tick(60) / 1000 #so enemie spawn isn't affected by framerate
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        fps_text = font.render(f"FPS: {clock.get_fps():.1f}", True, WHITE)
        frametime_text = font.render(f"frametime: {clock.get_time()} ms", True, WHITE)

        # UPDATE game state
        player.move()
        spawner.update(dt,enemies)
        for enemy in enemies:
            enemy.move_towards_player(player)


        # DRAW current game state
        screen.fill(BLACK) # fill the screen with a color to wipe away anything from last frame
        screen.blit(fps_text, (10, 10))
        screen.blit(frametime_text, (10, 30))

        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60

    pygame.quit()
if __name__ == "__main__":

    main()