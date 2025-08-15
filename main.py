from menu import show_menu
from game import play_game

def main():
    while True:
        difficulty = show_menu()
        if difficulty == False:
            break
        elif difficulty in ["easy", "medium", "hard"]:
            play_game(difficulty)

if __name__ == '__main__':
    main()