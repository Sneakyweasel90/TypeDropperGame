import pygame
import requests
from settings import WIDTH, HEIGHT, WHITE, BLACK, FONT
from animated_button import AnimatedButton

API_URL = "https://typedropperapi-1.onrender.com"


def run_leaderboards():
    while True:
        difficulty = show_leaderboards_menu()
        if difficulty is None:
            break
        show_leaderboard(difficulty)


def post_score_to_db(name, score, difficulty):
    try:
        r = requests.post(f"{API_URL}/typedropper/{difficulty}", json={
            "name": name,
            "score": score
        })
        if r.status_code != 200:
            print(f"Failed to save score: {r.status_code}")
    except Exception as e:
        print(f"Error posting score: {e}")


def load_leaderboard_from_db(difficulty):
    try:
        r = requests.get(f"{API_URL}/typedropper/{difficulty}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error loading leaderboard: {e}")
        return []


def is_high_score(score, difficulty):
    leaderboard = load_leaderboard_from_db(difficulty)
    if len(leaderboard) < 10:
        return True
    return score > leaderboard[-1]['score']


def show_leaderboards_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    button_easy = AnimatedButton(int(WIDTH * 0.25), int(HEIGHT * 0.45),
                                 int(WIDTH * 0.5), int(HEIGHT * 0.08),
                                 "Easy Leaderboard",
                                 color=(0, 200, 0), hover_color=(0, 255, 0))

    button_medium = AnimatedButton(int(WIDTH * 0.25), int(HEIGHT * 0.55),
                                   int(WIDTH * 0.5), int(HEIGHT * 0.08),
                                   "Medium Leaderboard",
                                   color=(255, 165, 0), hover_color=(255, 200, 0))

    button_hard = AnimatedButton(int(WIDTH * 0.25), int(HEIGHT * 0.65),
                                 int(WIDTH * 0.5), int(HEIGHT * 0.08),
                                 "Hard Leaderboard",
                                 color=(255, 69, 0), hover_color=(255, 100, 0))

    button_back = AnimatedButton(int(WIDTH * 0.4), int(HEIGHT * 0.85),
                                 int(WIDTH * 0.2), int(HEIGHT * 0.08),
                                 "Back",
                                 color=(100, 100, 100), hover_color=(150, 150, 150))

    buttons = {"easy": button_easy, "medium": button_medium, "hard": button_hard, "back": button_back}

    while True:
        dt = clock.tick(60) / 1000
        for b in buttons.values():
            b.update(dt)

        screen.fill(WHITE)
        title_text = FONT.render("Select Leaderboard", True, BLACK)
        screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.2))))

        for b in buttons.values():
            b.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            for diff, b in buttons.items():
                if b.handle_event(event):
                    if diff == "back":
                        return None
                    return diff

        pygame.display.flip()


def show_leaderboard(difficulty):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    button_back = AnimatedButton(int(WIDTH * 0.4), int(HEIGHT * 0.85),
                                 int(WIDTH * 0.2), int(HEIGHT * 0.08),
                                 "Back",
                                 color=(100, 100, 100), hover_color=(150, 150, 150))

    scores = load_leaderboard_from_db(difficulty)

    while True:
        dt = clock.tick(60) / 1000
        button_back.update(dt)

        screen.fill(WHITE)
        title_text = FONT.render(f"{difficulty.title()} Leaderboard", True, BLACK)
        screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.08))))

        header_font = pygame.font.Font(None, int(HEIGHT * 0.05))
        y_start = int(HEIGHT * 0.15)
        screen.blit(header_font.render("Rank", True, BLACK), (int(WIDTH * 0.3), y_start))
        screen.blit(header_font.render("Name", True, BLACK), (int(WIDTH * 0.5), y_start))
        screen.blit(header_font.render("Score", True, BLACK), (int(WIDTH * 0.7), y_start))

        entry_font = pygame.font.Font(None, int(HEIGHT * 0.04))
        y_offset = int(HEIGHT * 0.22)
        row_spacing = int(HEIGHT * 0.06)

        for i, entry in enumerate(scores[:10]):
            screen.blit(entry_font.render(f"{i + 1}.", True, BLACK), (int(WIDTH * 0.3), y_offset))
            screen.blit(entry_font.render(entry['name'], True, BLACK), (int(WIDTH * 0.5), y_offset))
            screen.blit(entry_font.render(str(entry['score']), True, BLACK), (int(WIDTH * 0.7), y_offset))
            y_offset += row_spacing

        button_back.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif button_back.handle_event(event):
                return

        pygame.display.flip()
