import os
import sys
import pygame, random
from settings import *
from utils import *
from animated_button import AnimatedButton

HIGH_SCORE_FILE = resource_path("assets/HIGH_SCORE.txt")

def load_highest_scores():
    default_scores = {'easy': 0, 'medium': 0, 'hard': 0}

    if not os.path.isfile(HIGH_SCORE_FILE):
        return default_scores

    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            content = f.read().strip()
            if content:
                scores = content.split(', ')
                if len(scores) >= 3:
                    return {
                        'easy': int(scores[0]),
                        'medium': int(scores[1]),
                        'hard': int(scores[2])
                    }
    except (ValueError, FileNotFoundError):
        pass

    return default_scores

def save_highest_scores(scores_dict):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(f"{scores_dict['easy']}, {scores_dict['medium']}, {scores_dict['hard']}")

def load_highest_score():
    scores = load_highest_scores()
    return max(scores.values())

def save_highest_score(score):
    scores = load_highest_scores()
    scores['easy'] = score
    save_highest_scores(scores)

def lose_screen(final_score, difficulty):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    high_scores = load_highest_scores()
    current_high_score = high_scores[difficulty]

    button_continue = AnimatedButton(
        WIDTH // 2 - 150, HEIGHT // 2, 300, 50,
        "Continue",
        color=(0, 200, 0),
        hover_color=(0, 255, 0)
    )

    is_new_highest_score = final_score > current_high_score

    if is_new_highest_score:
        high_scores[difficulty] = final_score
        save_highest_scores(high_scores)

    while True:

        dt = clock.tick(60) / 1000.0

        button_continue.update(dt)

        screen.fill(WHITE)

        text1 = FONT.render("Game Over!", True, BLACK)
        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT - 500))

        text2 = FONT.render("Final Score: " + str(final_score), True, BLACK)
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT - 400))

        difficulty_text = FONT.render(f"{difficulty.title()} Mode High Score: {high_scores[difficulty]}", True, BLACK)
        screen.blit(difficulty_text, (WIDTH // 2 - difficulty_text.get_width() // 2, HEIGHT - 350))

        if is_new_highest_score:
            new_record_text = FONT.render("NEW HIGHEST SCORE!", True, (255, 0, 0))
            screen.blit(new_record_text, (WIDTH // 2 - new_record_text.get_width() // 2, HEIGHT - 200))

        button_continue.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
            elif button_continue.handle_event(event):
                return True

        pygame.display.flip()