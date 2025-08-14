import pygame, random
from settings import *
from utils import load_words

def play_game():
    words = list(set(load_words("easyWords.txt")))
    last_word = None

    def get_random_word():
        nonlocal last_word
        word= random.choice(words)
        while word == last_word:
            word= random.choice(words)
        last_word = word
        return word

    current_word = get_random_word()
    word_x, word_y = random.randint(50, WIDTH - 150), 0
    typed_text = ""

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

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
                elif event.key == pygame.K_RETURN:
                    if typed_text.lower() == current_word.lower():
                        current_word = random.choice(words)
                        word_x, word_y = random.randint(50, WIDTH - 150), 0
                    typed_text = ""
                else:
                    typed_text += event.unicode

        word_y += FALL_SPEED
        if word_y > HEIGHT:
            current_word = random.choice(words)
            word_x, word_y = random.randint(50, WIDTH - 150), 0

        #draw word & typed text
        screen.blit(FONT.render(current_word, True, BLACK), (word_x, word_y))
        screen.blit(FONT.render(typed_text, True, BLACK), (20, HEIGHT - 50))

        pygame.display.flip()
        clock.tick(60)
