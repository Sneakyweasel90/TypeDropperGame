import pygame
from settings import WIDTH, HEIGHT, WHITE, BLACK, FONT, BACKGROUND_IMAGE

def show_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    while True:
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        text = FONT.render("Press SPACE to start", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True

        pygame.display.flip()
        clock.tick(60)