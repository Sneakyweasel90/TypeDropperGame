import pygame
from settings import *
from animated_button import AnimatedButton

def show_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    button_width = int(WIDTH * 0.5)
    button_height = int(HEIGHT * 0.08)
    button_x = int(WIDTH * 0.25)

    spacing = int(HEIGHT * 0.09)
    start_y = int(HEIGHT * 0.45)

    button_easy = AnimatedButton(
        button_x, start_y, button_width, button_height,
        "Easy Mode", color=(0, 200, 0), hover_color=(0, 255, 0)
    )
    button_medium = AnimatedButton(
        button_x, start_y + spacing, button_width, button_height,
        "Medium Mode", color=(255, 165, 0), hover_color=(255, 200, 0)
    )
    button_hard = AnimatedButton(
        button_x, start_y + spacing*2, button_width, button_height,
        "Hard Mode", color=(255, 69, 0), hover_color=(255, 100, 0)
    )
    button_leaderboard = AnimatedButton(
        button_x, start_y + spacing*3, button_width, button_height,
        "Show Leaderboards", color=(0, 100, 255), hover_color=(0, 150, 255)
    )

    buttons = [button_easy, button_medium, button_hard, button_leaderboard]
    difficulties = ["easy", "medium", "hard", "leaderboards"]

    title_font = pygame.font.Font(None, int(HEIGHT * 0.1))

    while True:
        dt = clock.tick(60) / 1000.0

        for button in buttons:
            button.update(dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            for i, button in enumerate(buttons):
                if button.handle_event(event):
                    return difficulties[i]

        screen.blit(pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT)), (0, 0))

        title = title_font.render("Type Dropper", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.2)))
        screen.blit(title, title_rect)

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
