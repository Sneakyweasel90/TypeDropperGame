import pygame, random
from settings import *
from utils import load_words
from loseScreen import lose_screen

def play_game(difficulty):
    if difficulty == "easy":
        words = list(set(load_words("assets/easyWords.txt")))
    elif difficulty == "medium":
        words = list(set(load_words("assets/mediumWords.txt")))
    else:
        words = list(set(load_words("assets/hardWords.txt")))

    last_word = None
    score = 0
    fall_speed = FALL_SPEED
    lives = 3

    def get_random_word():
        nonlocal last_word
        word = random.choice(words)
        while word == last_word:
            word = random.choice(words)
        last_word = word
        return word

    current_word = get_random_word()
    word_x, word_y = random.randint(50, WIDTH - 150), 0
    typed_text = ""

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    waiting = True
    while waiting:
        screen.fill(WHITE)
        message = FONT.render("Press 'SPACE' to start!", True, BLACK)
        msg_rect = message.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(message, msg_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_SPACE:
                    waiting = False
        clock.tick(60)

    for count in range(3, 0, -1):
        screen.fill(WHITE)
        countdown_text = FONT.render(str(count), True, BLACK)
        text_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(countdown_text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)

    while True:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]
                elif event.unicode.isalpha():
                    typed_text += event.unicode

        if typed_text.lower() == current_word.lower():
            score += 100
            fall_speed += 0.1
            current_word = get_random_word()
            word_x, word_y = random.randint(50, WIDTH - 150), 0
            typed_text = ""

        word_y += fall_speed
        if word_y > HEIGHT:
            lives -= 1
            current_word = get_random_word()
            word_x, word_y = random.randint(50, WIDTH - 150), 0
            typed_text = ""

        if lives <= 0:
            return lose_screen(score, difficulty)

        x_offset = 0
        for i, letter in enumerate(current_word):
            color = BLACK
            if i < len(typed_text):
                if typed_text[i].lower() == letter.lower():
                    color = (0, 200, 0)
                else:
                    color = (200, 0, 0)
            letter_surface = FONT.render(letter, True, color)
            screen.blit(letter_surface, (word_x + x_offset, word_y))
            x_offset += letter_surface.get_width()

        screen.blit(FONT.render(typed_text, True, BLACK), (20, HEIGHT - 50))
        screen.blit(FONT.render(f"Score: {score}", True, BLACK), (WIDTH - 200, 20))
        screen.blit(FONT.render(f"Speed: {fall_speed:.1f}", True, BLACK), (WIDTH - 500, 20))
        screen.blit(FONT.render(f"Lives: {lives}", True, BLACK), (WIDTH - 800, 20))

        pygame.display.flip()
        clock.tick(60)
