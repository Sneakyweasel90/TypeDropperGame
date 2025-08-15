import pygame.display

from menu import show_menu
from game import play_game

def main():

    pygame.display.set_caption('Type Dropper')
    while True:
        difficulty = show_menu()
        if not difficulty:
            break
        elif difficulty in ["easy", "medium", "hard"]:
            play_game(difficulty)

if __name__ == '__main__':
    main()