import os
import sys
import pygame, random
from settings import *

def lose_screen(final_score):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)
        text1 = FONT.render("Game Over!", True, BLACK)
        text2 = FONT.render("Final Score: " + str(final_score), True, BLACK)
        text3 = FONT.render("Press Space to continue", True, BLACK)

        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 3))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2))
        screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 1.5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True

        pygame.display.flip()
        clock.tick(60)