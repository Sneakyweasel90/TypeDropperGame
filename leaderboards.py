import os
import sys
import pygame
from pymongo import MongoClient
from pathlib import Path
from dotenv import load_dotenv
from settings import WIDTH, HEIGHT, WHITE, BLACK, FONT
from animated_button import AnimatedButton

base_path = getattr(sys, "_MEIPASS", Path(__file__).parent)
dotenv_path = Path(base_path) / ".env"
load_dotenv(dotenv_path=dotenv_path)

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB = os.getenv("MONGO_DB")

if None in [MONGO_USER, MONGO_PASSWORD, MONGO_DB]:
    raise ValueError("MongoDB credentials missing! Check your .env or environment variables.")

MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@typedropperapi.mkvil3t.mongodb.net/{MONGO_DB}?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
scores_collection = db["scores"]

def run_leaderboards():
    while True:
        difficulty = show_leaderboards_menu()
        if difficulty is None:
            break

        show_leaderboard(difficulty)

def post_score_to_db(name, score, difficulty):
    try:
        data = {"name": name, "score": score, "difficulty": difficulty}
        result = scores_collection.insert_one(data)
        print(f"Score saved with id: {result.inserted_id}")
    except Exception as e:
        print(f"Error saving score to DB: {e}")

def load_leaderboard_from_db(difficulty):
    try:
        leaderboard = list(scores_collection.find({"difficulty": difficulty}).sort("score", -1).limit(10))
        return [{"name": e["name"], "score": e["score"], "difficulty": e["difficulty"]} for e in leaderboard]
    except Exception as e:
        print(f"Error loading leaderboard: {e}")
        return []

def is_high_score(score, difficulty):
    leaderboard = load_leaderboard_from_db(difficulty)
    if len(leaderboard) < 10:
        return True
    return score > leaderboard[-1]['score']

def show_leaderboards_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    button_easy = AnimatedButton(WIDTH//2 - 200, HEIGHT//2 - 60, 400, 50,
                                 "Easy Leaderboard", color=(0,200,0), hover_color=(0,255,0))
    button_medium = AnimatedButton(WIDTH//2 - 200, HEIGHT//2, 400, 50,
                                   "Medium Leaderboard", color=(255,165,0), hover_color=(255,200,0))
    button_hard = AnimatedButton(WIDTH//2 - 200, HEIGHT//2 + 60, 400, 50,
                                 "Hard Leaderboard", color=(255,69,0), hover_color=(255,100,0))
    button_back = AnimatedButton(WIDTH//2 - 75, HEIGHT - 80, 150, 50,
                                 "Back", color=(100,100,100), hover_color=(150,150,150))

    buttons = {
        "easy": button_easy,
        "medium": button_medium,
        "hard": button_hard,
        "back": button_back
    }

    while True:
        dt = clock.tick(60)/1000
        for b in buttons.values():
            b.update(dt)

        screen.fill(WHITE)
        title_text = FONT.render("Select Leaderboard", True, BLACK)
        screen.blit(title_text, title_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 150)))

        for b in buttons.values():
            b.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None

            for diff, b in buttons.items():
                if b.handle_event(event):
                    if diff == "back":
                        return None
                    return diff

        pygame.display.flip()


def show_leaderboard(difficulty):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    button_back = AnimatedButton(WIDTH//2 - 75, HEIGHT - 80, 150, 50,
                                 "Back", color=(100,100,100), hover_color=(150,150,150))

    scores = load_leaderboard_from_db(difficulty)

    while True:
        dt = clock.tick(60)/1000
        button_back.update(dt)

        screen.fill(WHITE)
        title_text = FONT.render(f"{difficulty.title()} Leaderboard", True, BLACK)
        screen.blit(title_text, title_text.get_rect(center=(WIDTH//2, 50)))

        header_font = pygame.font.Font(None, 36)
        screen.blit(header_font.render("Rank", True, BLACK), (WIDTH//2-200, 100))
        screen.blit(header_font.render("Name", True, BLACK), (WIDTH//2-50, 100))
        screen.blit(header_font.render("Score", True, BLACK), (WIDTH//2+100, 100))

        entry_font = pygame.font.Font(None, 32)
        y_offset = 140
        for i, entry in enumerate(scores[:10]):
            screen.blit(entry_font.render(f"{i+1}.", True, BLACK), (WIDTH//2-200, y_offset))
            screen.blit(entry_font.render(entry['name'], True, BLACK), (WIDTH//2-50, y_offset))
            screen.blit(entry_font.render(str(entry['score']), True, BLACK), (WIDTH//2+100, y_offset))
            y_offset += 35

        button_back.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif button_back.handle_event(event):
                return

        pygame.display.flip()
