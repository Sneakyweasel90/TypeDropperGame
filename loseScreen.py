import pygame
import requests
from settings import *
from animated_button import AnimatedButton

API_URL = "https://typedropperapi-1.onrender.com"


def post_score_to_db(name, score, difficulty):
    try:
        r = requests.post(f"{API_URL}/typedropper/{difficulty}", json={
            "name": name,
            "score": score
        })
        if r.status_code == 200:
            print("Score saved successfully!")
        else:
            print(f"Failed to save score: {r.status_code} {r.text}")
    except Exception as e:
        print(f"Error saving score to API: {e}")


def load_leaderboard_from_db(difficulty):
    try:
        r = requests.get(f"{API_URL}/typedropper/{difficulty}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error fetching leaderboard from API: {e}")
        return []


def is_high_score(score, difficulty):
    leaderboard = load_leaderboard_from_db(difficulty)
    if len(leaderboard) < 10:
        return True
    return score > leaderboard[-1]['score']


def get_player_name(score, difficulty):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player_name = ""
    cursor_visible = True
    cursor_timer = 0

    title_font = pygame.font.Font(None, int(HEIGHT * 0.1))
    score_font = pygame.font.Font(None, int(HEIGHT * 0.07))
    instruction_font = pygame.font.Font(None, int(HEIGHT * 0.05))
    name_font = pygame.font.Font(None, int(HEIGHT * 0.12))
    bottom_font = pygame.font.Font(None, int(HEIGHT * 0.04))

    banned_words = ["kkk", "gay", "fag", "fuk", "fuc", "ass", "nig", "f@g", "tit"]
    bottom_text = "Type letters to enter name, ESC to cancel"
    invalid_name_warning = False

    while True:
        screen.blit(pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT)), (0, 0))

        screen.blit(title_font.render("NEW HIGH SCORE!", True, (255, 0, 0)),
                    title_font.render("NEW HIGH SCORE!", True, (255, 0, 0)).get_rect(center=(WIDTH//2, int(HEIGHT*0.2))))
        screen.blit(score_font.render(f"Score: {score} ({difficulty.title()} Mode)", True, BLACK),
                    score_font.render(f"Score: {score} ({difficulty.title()} Mode)", True, BLACK).get_rect(center=(WIDTH//2, int(HEIGHT*0.3))))
        screen.blit(instruction_font.render("Enter your 3-letter name:", True, BLACK),
                    instruction_font.render("Enter your 3-letter name:", True, BLACK).get_rect(center=(WIDTH//2, int(HEIGHT*0.38))))

        display_name = player_name.ljust(3, '_')
        cursor_timer += clock.get_time()
        if cursor_timer > 500:
            cursor_visible = not cursor_visible
            cursor_timer = 0
        if cursor_visible and len(player_name) < 3:
            display_name = display_name[:len(player_name)] + '|' + display_name[len(player_name)+1:]
        screen.blit(name_font.render(display_name, True, BLACK),
                    name_font.render(display_name, True, BLACK).get_rect(center=(WIDTH//2, int(HEIGHT*0.5))))

        screen.blit(bottom_font.render(bottom_text, True, BLACK),
                    bottom_font.render(bottom_text, True, BLACK).get_rect(center=(WIDTH//2, int(HEIGHT*0.65))))

        pygame.display.flip()

        enter_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_RETURN and len(player_name) == 3:
                    enter_pressed = True
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                    invalid_name_warning = False
                elif len(player_name) < 3 and event.unicode.isalpha():
                    player_name += event.unicode.upper()
                    invalid_name_warning = False

        if enter_pressed:
            if player_name.lower() in banned_words:
                bottom_text = "This name is not allowed!"
                invalid_name_warning = True
            else:
                return player_name.upper()

        if not invalid_name_warning:
            if len(player_name) == 3:
                bottom_text = "Press ENTER to save, ESC to cancel"
            else:
                bottom_text = "Type letters to enter name, ESC to cancel"

        clock.tick(60)


def show_leaderboard(difficulty):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    button_back = AnimatedButton(int(WIDTH*0.4), int(HEIGHT*0.85),
                                 int(WIDTH*0.2), int(HEIGHT*0.08),
                                 "Back", color=(100,100,100), hover_color=(150,150,150))

    difficulty_scores = load_leaderboard_from_db(difficulty)

    while True:
        dt = clock.tick(60)/1000
        button_back.update(dt)
        screen.blit(pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT)), (0, 0))

        title_font = pygame.font.Font(None, int(HEIGHT*0.08))
        screen.blit(title_font.render(f"{difficulty.title()} Mode Leaderboard", True, BLACK),
                    title_font.render(f"{difficulty.title()} Mode Leaderboard", True, BLACK).get_rect(center=(WIDTH//2, int(HEIGHT*0.08))))

        header_font = pygame.font.Font(None, int(HEIGHT*0.05))
        y_start = int(HEIGHT * 0.15)
        screen.blit(header_font.render("Rank", True, BLACK), (int(WIDTH*0.3), y_start))
        screen.blit(header_font.render("Name", True, BLACK), (int(WIDTH*0.5), y_start))
        screen.blit(header_font.render("Score", True, BLACK), (int(WIDTH*0.7), y_start))

        entry_font = pygame.font.Font(None, int(HEIGHT*0.04))
        y_offset = int(HEIGHT*0.22)
        row_spacing = int(HEIGHT*0.06)
        for i, entry in enumerate(difficulty_scores[:10]):
            screen.blit(entry_font.render(f"{i+1}.", True, BLACK), (int(WIDTH*0.3), y_offset))
            screen.blit(entry_font.render(entry['name'], True, BLACK), (int(WIDTH*0.5), y_offset))
            screen.blit(entry_font.render(str(entry['score']), True, BLACK), (int(WIDTH*0.7), y_offset))
            y_offset += row_spacing

        button_back.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            elif button_back.handle_event(event):
                return False

        pygame.display.flip()


def lose_screen(final_score, difficulty):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.blit(pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT)), (0, 0))

    player_name = None
    if is_high_score(final_score, difficulty):
        player_name = get_player_name(final_score, difficulty)
        if player_name:
            post_score_to_db(player_name, final_score, difficulty)

    leaderboard = load_leaderboard_from_db(difficulty)
    current_high_score = max([entry['score'] for entry in leaderboard], default=0)

    y_game_over = int(HEIGHT*0.2)
    y_final_score = int(HEIGHT*0.3)
    y_difficulty = int(HEIGHT*0.38)
    y_saved = int(HEIGHT*0.46)

    button_continue = AnimatedButton(int(WIDTH*0.35), int(HEIGHT*0.55),
                                     int(WIDTH*0.3), int(HEIGHT*0.08),
                                     "Continue", color=(0,200,0), hover_color=(0,255,0))

    button_leaderboard = AnimatedButton(int(WIDTH*0.35), int(HEIGHT*0.65),
                                        int(WIDTH*0.3), int(HEIGHT*0.08),
                                        "View Leaderboard", color=(0,100,200), hover_color=(0,150,255))

    while True:
        dt = clock.tick(60)/1000
        button_continue.update(dt)
        button_leaderboard.update(dt)
        screen.blit(pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT)), (0, 0))

        screen.blit(FONT.render("Game Over!", True, BLACK),
                    (WIDTH//2 - FONT.size("Game Over!")[0]//2, y_game_over))
        screen.blit(FONT.render(f"Final Score: {final_score}", True, BLACK),
                    (WIDTH//2 - FONT.size(f"Final Score: {final_score}")[0]//2, y_final_score))
        screen.blit(FONT.render(f"{difficulty.title()} Mode High Score: {current_high_score}", True, BLACK),
                    (WIDTH//2 - FONT.size(f"{difficulty.title()} Mode High Score: {current_high_score}")[0]//2, y_difficulty))

        if player_name:
            saved_text = FONT.render(f"Score saved as {player_name}!", True, (0,150,0))
            screen.blit(saved_text, (WIDTH//2 - saved_text.get_width()//2, y_saved))
        elif is_high_score(final_score, difficulty) and not player_name:
            missed_text = FONT.render("High score not saved", True, (150,150,0))
            screen.blit(missed_text, (WIDTH//2 - missed_text.get_width()//2, y_saved))

        button_continue.draw(screen)
        button_leaderboard.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_l:
                    show_leaderboard(difficulty)
            elif button_continue.handle_event(event):
                return True
            elif button_leaderboard.handle_event(event):
                show_leaderboard(difficulty)

        pygame.display.flip()
