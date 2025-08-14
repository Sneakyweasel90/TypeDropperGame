import os
import sys
import pygame, random
from settings import *
from utils import *

HIGH_SCORE_FILE = resource_path("assets/HIGH_SCORE.txt")

def load_highest_score():
    if not os.path.isfile(HIGH_SCORE_FILE):
        return 0
    with open(HIGH_SCORE_FILE) as f:
        return int(f.read().strip())

def save_highest_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

def lose_screen(final_score):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    highest_score = load_highest_score()

    if final_score > highest_score:
        highest_score = final_score
        save_highest_score(highest_score)

    while True:
        screen.fill(WHITE)
        text1 = FONT.render("Game Over!", True, BLACK)
        text2 = FONT.render("Final Score: " + str(final_score), True, BLACK)
        text3 = FONT.render(f"Highest Score {highest_score}", True, BLACK)
        text4 = FONT.render("Press Space to continue", True, BLACK)

        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT - 500))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT - 400))
        screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT - 300))
        screen.blit(text4, (WIDTH // 2 - text4.get_width() // 2, HEIGHT - 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True

        pygame.display.flip()
        clock.tick(60)