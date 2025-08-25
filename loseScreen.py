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

    while True:
        screen.fill(WHITE)

        title_text = FONT.render("NEW HIGH SCORE!", True, (255, 0, 0))
        screen.blit(title_text, title_text.get_rect(center=(WIDTH//2, HEIGHT//2-120)))
        score_text = FONT.render(f"Score: {score} ({difficulty.title()} Mode)", True, BLACK)
        screen.blit(score_text, score_text.get_rect(center=(WIDTH//2, HEIGHT//2-70)))
        instruction_text = FONT.render("Enter your 3-letter name:", True, BLACK)
        screen.blit(instruction_text, instruction_text.get_rect(center=(WIDTH//2, HEIGHT//2-20)))

        display_name = player_name.ljust(3, '_')
        cursor_timer += clock.get_time()
        if cursor_timer > 500:
            cursor_visible = not cursor_visible
            cursor_timer = 0
        if cursor_visible and len(player_name) < 3:
            display_name = display_name[:len(player_name)] + '|' + display_name[len(player_name)+1:]

        name_text = pygame.font.Font(None, 72).render(display_name, True, BLACK)
        screen.blit(name_text, name_text.get_rect(center=(WIDTH//2, HEIGHT//2+30)))

        if len(player_name) == 3:
            bottom_text = FONT.render("Press ENTER to save, ESC to cancel", True, BLACK)
        else:
            bottom_text = FONT.render("Type letters to enter name, ESC to cancel", True, BLACK)
        screen.blit(bottom_text, bottom_text.get_rect(center=(WIDTH//2, HEIGHT//2+100)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_RETURN and len(player_name) == 3:
                    return player_name.upper()
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 3 and event.unicode.isalpha():
                    player_name += event.unicode.upper()

        clock.tick(60)

def show_leaderboard(difficulty):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    button_back = AnimatedButton(WIDTH//2-75, HEIGHT-100, 150, 50, "Back", color=(100,100,100), hover_color=(150,150,150))

    difficulty_scores = load_leaderboard_from_db(difficulty)

    while True:
        dt = clock.tick(60)/1000
        button_back.update(dt)
        screen.fill(WHITE)

        title_text = FONT.render(f"{difficulty.title()} Mode Leaderboard", True, BLACK)
        screen.blit(title_text, title_text.get_rect(center=(WIDTH//2, 50)))

        header_font = pygame.font.Font(None, 36)
        screen.blit(header_font.render("Rank", True, BLACK), (WIDTH//2-200, 100))
        screen.blit(header_font.render("Name", True, BLACK), (WIDTH//2-50, 100))
        screen.blit(header_font.render("Score", True, BLACK), (WIDTH//2+100, 100))

        entry_font = pygame.font.Font(None, 32)
        y_offset = 140
        for i, entry in enumerate(difficulty_scores[:10]):
            screen.blit(entry_font.render(f"{i+1}.", True, BLACK), (WIDTH//2-200, y_offset))
            screen.blit(entry_font.render(entry['name'], True, BLACK), (WIDTH//2-50, y_offset))
            screen.blit(entry_font.render(str(entry['score']), True, BLACK), (WIDTH//2+100, y_offset))
            y_offset += 35

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

    player_name = None
    if is_high_score(final_score, difficulty):
        player_name = get_player_name(final_score, difficulty)
        if player_name:
            post_score_to_db(player_name, final_score, difficulty)

    leaderboard = load_leaderboard_from_db(difficulty)
    current_high_score = max([entry['score'] for entry in leaderboard], default=0)

    y_text = HEIGHT - 500
    text_positions = {
        'game_over': y_text,
        'final_score': y_text+100,
        'difficulty': y_text+150,
        'saved': y_text+200
    }

    button_continue = AnimatedButton(WIDTH//2-150, y_text+260, 300, 50, "Continue", color=(0,200,0), hover_color=(0,255,0))
    button_leaderboard = AnimatedButton(WIDTH//2-150, y_text+330, 300, 50, "View Leaderboard", color=(0,100,200), hover_color=(0,150,255))

    while True:
        dt = clock.tick(60)/1000
        button_continue.update(dt)
        button_leaderboard.update(dt)
        screen.fill(WHITE)

        screen.blit(FONT.render("Game Over!", True, BLACK), (WIDTH//2-FONT.size("Game Over!")[0]//2, text_positions['game_over']))
        screen.blit(FONT.render(f"Final Score: {final_score}", True, BLACK), (WIDTH//2-FONT.size(f"Final Score: {final_score}")[0]//2, text_positions['final_score']))
        screen.blit(FONT.render(f"{difficulty.title()} Mode High Score: {current_high_score}", True, BLACK),
                    (WIDTH//2-FONT.size(f"{difficulty.title()} Mode High Score: {current_high_score}")[0]//2, text_positions['difficulty']))

        if player_name:
            saved_text = FONT.render(f"Score saved as {player_name}!", True, (0,150,0))
            screen.blit(saved_text, (WIDTH//2-saved_text.get_width()//2, text_positions['saved']))
        elif is_high_score(final_score, difficulty) and not player_name:
            missed_text = FONT.render("High score not saved", True, (150,150,0))
            screen.blit(missed_text, (WIDTH//2-missed_text.get_width()//2, text_positions['saved']))

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
