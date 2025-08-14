from menu import show_menu
from game import play_game

def main():
    while True:
        start_game = show_menu()
        if start_game:
            play_game()
        else:
            break #this will exit the game

if __name__ == '__main__':
    main()