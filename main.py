# Example file showing a basic pygame "game loop"
import pygame
from constants import *
from player import Player


def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None,36)
    clock = pygame.time.Clock()
    running = True

    # Create player once outside the loop
    player = Player(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        fps_text = font.render(f"FPS: {clock.get_fps():.1f}", True, "white")

        # Update player position
        player.move()
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill(BLACK)
        screen.blit(fps_text, (10, 10))
        # RENDER YOUR GAME HERE
        player.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
if __name__ == "__main__":

    main()