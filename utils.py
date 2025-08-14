def load_words(filepath):
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]
