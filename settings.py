import pygame
from utils import resource_path

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FALL_SPEED = 5
BACKGROUND_IMAGE = pygame.image.load(resource_path("assets/TypeDropper.png"))

pygame.font.init()
FONT = pygame.font.Font(None, 48)