import pygame
from settings import WIDTH, HEIGHT, WHITE, BLACK, FONT, BACKGROUND_IMAGE
from animated_button import AnimatedButton

def show_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    button_easy = AnimatedButton(
        WIDTH // 2 - 200, HEIGHT // 2, 400, 50,
        "Easy Mode",
        color=(0, 200, 0),
        hover_color=(0, 255, 0)
    )

    button_medium = AnimatedButton(
        WIDTH // 2 - 200, HEIGHT // 2 + 70, 400, 50,
        "Medium Mode",
        color=(255, 165, 0),
        hover_color=(255, 200, 0)
    )

    button_hard = AnimatedButton(
        WIDTH // 2 - 200, HEIGHT // 2 + 140, 400, 50,
        "Hard Mode",
        color=(255, 69, 0),
        hover_color=(255, 100, 0)
    )

    button_leaderboard = AnimatedButton(
        WIDTH // 2 - 200, HEIGHT // 2 + 210, 400, 50,
        "Show Leaderboards",
        color=(0, 100, 255),
        hover_color=(0, 150, 255)
    )

    buttons = [button_easy, button_medium, button_hard, button_leaderboard]
    difficulties = ["easy", "medium", "hard", "leaderboards"]

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

        screen.blit(BACKGROUND_IMAGE, (0, 0))

        title = FONT.render("Type Dropper", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(title, title_rect)

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
