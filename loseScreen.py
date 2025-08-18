import os
import sys
from operator import itemgetter
import pygame, random
from settings import *
from utils import *
from animated_button import AnimatedButton

HIGH_SCORE_FILE = resource_path("assets/HIGH_SCORE.txt")

def load_leaderboard():
    default_leaderboard = []

    if not os.path.isfile(HIGH_SCORE_FILE):
        return default_leaderboard

    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            content = f.read().strip()
            if content:
                entries = content.split(';')
                leaderboard = []
                for entry in entries:
                    if entry.strip():
                        parts = entry.split(',')
                        if len(parts) == 3:
                            name, score, difficulty = parts
                            leaderboard.append({
                                'name': name.strip(),
                                'score': int(score.strip()),
                                'difficulty': difficulty.strip()
                            })
                return sorted(leaderboard, key=itemgetter('score'), reverse=True)
    except (ValueError, FileNotFoundError, IndexError):
        pass

    return default_leaderboard

def save_leaderboard(leaderboard):
    with open(HIGH_SCORE_FILE, 'w') as f:
        entries = []
        for entry in leaderboard:
            entries.append(f"{entry['name']},{entry['score']},{entry['difficulty']}")
        f.write(';'.join(entries))

def is_high_score(score, difficulty):
    leaderboard = load_leaderboard()
    difficulty_scores = [entry for entry in leaderboard if entry['difficulty'] == difficulty]

    if len(difficulty_scores) < 10:
        return True

    difficulty_scores.sort(key=itemgetter('score'), reverse=True)
    return score > difficulty_scores[9]['score']

def get_player_name(score, difficulty):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player_name = ""
    cursor_visible = True
    cursor_timer = 0

    while True:
        screen.fill(WHITE)

        title_text = FONT.render("NEW HIGH SCORE!", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
        screen.blit(title_text, title_rect)

        score_text = FONT.render(f"Score: {score} ({difficulty.title()} Mode)", True, BLACK)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70))
        screen.blit(score_text, score_rect)

        instruction_text = FONT.render("Enter your 3-letter name:", True, BLACK)
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(instruction_text, instruction_rect)

        display_name = player_name.ljust(3, '_')
        cursor_timer += clock.get_time()
        if cursor_timer > 500:  # Blink every 500ms
            cursor_visible = not cursor_visible
            cursor_timer = 0

        if cursor_visible and len(player_name) < 3:
            display_name = display_name[:len(player_name)] + '|' + display_name[len(player_name) + 1:]

        name_text = pygame.font.Font(None, 72).render(display_name, True, BLACK)
        name_rect = name_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        screen.blit(name_text, name_rect)

        if len(player_name) == 3:
            bottom_text = FONT.render("Press ENTER to save, ESC to cancel", True, BLACK)
        else:
            bottom_text = FONT.render("Type letters to enter name, ESC to cancel", True, BLACK)
        bottom_rect = bottom_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(bottom_text, bottom_rect)

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

    button_back = AnimatedButton(
        WIDTH // 2 - 75, HEIGHT - 100, 150, 50,
        "Back",
        color=(100, 100, 100),
        hover_color=(150, 150, 150)
    )

    leaderboard = load_leaderboard()
    difficulty_scores = [entry for entry in leaderboard if entry['difficulty'] == difficulty]
    difficulty_scores = sorted(difficulty_scores, key=itemgetter('score'), reverse=True)[:10]

    while True:
        dt = clock.tick(60) / 1000.0
        button_back.update(dt)

        screen.fill(WHITE)

        title_text = FONT.render(f"{difficulty.title()} Mode Leaderboard", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        header_font = pygame.font.Font(None, 36)
        rank_header = header_font.render("Rank", True, BLACK)
        name_header = header_font.render("Name", True, BLACK)
        score_header = header_font.render("Score", True, BLACK)

        screen.blit(rank_header, (WIDTH // 2 - 200, 100))
        screen.blit(name_header, (WIDTH // 2 - 50, 100))
        screen.blit(score_header, (WIDTH // 2 + 100, 100))

        entry_font = pygame.font.Font(None, 32)
        y_offset = 140

        for i, entry in enumerate(difficulty_scores):
            if i >= 10:
                break

            rank_text = entry_font.render(f"{i + 1}.", True, BLACK)
            name_text = entry_font.render(entry['name'], True, BLACK)
            score_text = entry_font.render(str(entry['score']), True, BLACK)

            screen.blit(rank_text, (WIDTH // 2 - 200, y_offset))
            screen.blit(name_text, (WIDTH // 2 - 50, y_offset))
            screen.blit(score_text, (WIDTH // 2 + 100, y_offset))

            y_offset += 35

        if not difficulty_scores:
            no_scores_text = FONT.render("No scores yet!", True, BLACK)
            no_scores_rect = no_scores_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(no_scores_text, no_scores_rect)

        button_back.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif button_back.handle_event(event):
                return

        pygame.display.flip()

def lose_screen(final_score, difficulty):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player_name = None
    if is_high_score(final_score, difficulty):
        player_name = get_player_name(final_score, difficulty)

        if player_name:
            leaderboard = load_leaderboard()
            leaderboard.append({
                'name': player_name,
                'score': final_score,
                'difficulty': difficulty
            })

            difficulty_entries = [entry for entry in leaderboard if entry['difficulty'] == difficulty]
            difficulty_entries.sort(key=itemgetter('score'), reverse=True)
            difficulty_entries = difficulty_entries[:10]

            other_entries = [entry for entry in leaderboard if entry['difficulty'] != difficulty]
            leaderboard = other_entries + difficulty_entries

            save_leaderboard(leaderboard)

    leaderboard = load_leaderboard()
    difficulty_scores = [entry for entry in leaderboard if entry['difficulty'] == difficulty]
    current_high_score = max([entry['score'] for entry in difficulty_scores], default=0)

    y_text = HEIGHT - 500
    text_positions = {}

    text_positions['game_over'] = y_text
    y_text += 100

    text_positions['final_score'] = y_text
    y_text += 50

    text_positions['difficulty'] = y_text
    y_text += 50

    text_positions['saved'] = y_text
    y_text += 60

    button_continue = AnimatedButton(
        WIDTH // 2 - 150, y_text, 300, 50,
        "Continue",
        color=(0, 200, 0),
        hover_color=(0, 255, 0)
    )

    button_leaderboard = AnimatedButton(
        WIDTH // 2 - 150, y_text + 70, 300, 50,
        "View Leaderboard",
        color=(0, 100, 200),
        hover_color=(0, 150, 255)
    )

    while True:
        dt = clock.tick(60) / 1000.0
        button_continue.update(dt)
        button_leaderboard.update(dt)

        screen.fill(WHITE)

        text1 = FONT.render("Game Over!", True, BLACK)
        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, text_positions['game_over']))

        text2 = FONT.render("Final Score: " + str(final_score), True, BLACK)
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, text_positions['final_score']))

        difficulty_text = FONT.render(f"{difficulty.title()} Mode High Score: {current_high_score}", True, BLACK)
        screen.blit(difficulty_text, (WIDTH // 2 - difficulty_text.get_width() // 2, text_positions['difficulty']))

        if player_name:
            saved_text = FONT.render(f"Score saved as {player_name}!", True, (0, 150, 0))
            screen.blit(saved_text, (WIDTH // 2 - saved_text.get_width() // 2, text_positions['saved']))
        elif is_high_score(final_score, difficulty) and not player_name:
            missed_text = FONT.render("High score not saved", True, (150, 150, 0))
            screen.blit(missed_text, (WIDTH // 2 - missed_text.get_width() // 2, text_positions['saved']))

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