import pygame
from utils import resource_path

pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

WIDTH = int(SCREEN_WIDTH * 0.8)
HEIGHT = int(SCREEN_HEIGHT * 0.8)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FALL_SPEED = int(HEIGHT * 0.003)

BACKGROUND_IMAGE = pygame.image.load(resource_path("assets/gradient-toxic.jpg"))
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

pygame.font.init()
FONT = pygame.font.Font(None, int(HEIGHT * 0.08))
