import pygame.display
from menu import show_menu
from game import play_game
from leaderboards import *

def main():
    pygame.display.set_caption('Type Dropper')

    while True:
        difficulty = show_menu()
        if not difficulty:
            break

        if difficulty in ["easy", "medium", "hard"]:
            play_game(difficulty)

        elif difficulty == "leaderboards":
            run_leaderboards()

if __name__ == '__main__':
    main()