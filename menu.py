import pygame
from settings import WIDTH, HEIGHT, WHITE, BLACK, FONT, BACKGROUND_IMAGE

def show_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)

    while True:
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        #button
        pygame.draw.rect(screen, (0, 200, 0), button_rect)
        text = FONT.render("Easy Mode", True, BLACK)
        screen.blit(text, (button_rect.x + (button_rect.width - text.get_width()) // 2,
                           button_rect.y + (button_rect.height - text.get_height()) // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    return True

        pygame.display.flip()
        clock.tick(60)