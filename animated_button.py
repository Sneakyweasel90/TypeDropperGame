import pygame
import math
from settings import FONT, BLACK

class AnimatedButton:
    def __init__(self, x, y, width, height, text, color=(0, 200, 0), hover_color=(0, 255, 0), text_color=BLACK):
        self.original_rect = pygame.Rect(x, y, width, height)
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

        self.is_hovered = False
        self.is_pressed = False
        self.hover_scale = 1.0
        self.target_scale = 1.0
        self.pulse_time = 0

        self.text_surface = FONT.render(text, True, text_color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.original_rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.original_rect.collidepoint(event.pos):
                self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.is_pressed and self.original_rect.collidepoint(event.pos):
                    self.is_pressed = False
                    return True
                self.is_pressed = False
        return False

    def update(self, dt):
        self.pulse_time += dt * 3

        if self.is_pressed:
            self.target_scale = 0.95
        elif self.is_hovered:
            self.target_scale = 1.05
        else:
            self.target_scale = 1.0

        self.hover_scale += (self.target_scale - self.hover_scale) * 0.2

        center = self.original_rect.center
        new_width = int(self.original_rect.width * self.hover_scale)
        new_height = int(self.original_rect.height * self.hover_scale)
        self.rect = pygame.Rect(0, 0, new_width, new_height)
        self.rect.center = center

    def draw(self, screen):
        if self.is_hovered:
            pulse = math.sin(self.pulse_time) * 0.1 + 0.9
            color = tuple(min(255, int(c * pulse)) for c in self.hover_color)
        else:
            color = self.color

        if not self.is_pressed:
            shadow_rect = self.rect.copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=10)

        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=10)

        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)