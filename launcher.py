import requests
import os
import subprocess
import hashlib

API_URL = "https://api.github.com/repos/Sneakyweasel90/TypeDropperGame/releases/latest"
GAME_FILE = "main.exe"
LOCAL_VERSION_FILE = "game_version.txt"

def get_local_version():
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
    return "0.0.0"

def set_local_version(version):
    with open(LOCAL_VERSION_FILE, "w") as f:
        f.write(version)

def check_latest_release():
    """Fetch latest release info from GitHub."""
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    data = r.json()

    latest_version = data["tag_name"]
    exe_url, hash_url = None, None

    for asset in data["assets"]:
        name = asset["name"].lower()
        if name == "main.exe":
            exe_url = asset["browser_download_url"]
        elif name == "main.sha256":
            hash_url = asset["browser_download_url"]

    return latest_version, exe_url, hash_url

def download_file(url, filename):
    """Download a file and save it locally."""
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    with open(filename, "wb") as f:
        f.write(r.content)

def calculate_sha256(filename):
    """Return the SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def attempt_update(exe_url, hash_url):
    try:
        print("Downloading new version of the game...")
        download_file(exe_url, GAME_FILE)

        if hash_url:
            print("Verifying integrity...")
            download_file(hash_url, "main.sha256")

            with open("main.sha256", "r") as f:
                expected_hash = f.read().strip().split()[0]

            actual_hash = calculate_sha256(GAME_FILE)
            if actual_hash != expected_hash:
                print("Hash mismatch! Download may be corrupted or tampered.")
                os.remove(GAME_FILE)
                return False
            print("Hash verified successfully")
        else:
            print("No checksum file provided. Skipping verification.")

        return True
    except Exception as e:
        print("Update failed:", e)
        return False

def launch_game():
    if os.path.exists(GAME_FILE):
        print("Starting game...")
        subprocess.Popen([GAME_FILE], shell=True)
    else:
        print("Game executable not found! Please re-download launcher.")

def main():
    local_version = get_local_version()

    try:
        latest_version, exe_url, hash_url = check_latest_release()
    except Exception as e:
        print("Could not check for updates:", e)
        if not os.path.exists(GAME_FILE):
            print("Game not installed and no connection. Exiting.")
            return
        launch_game()
        return

    if not os.path.exists(GAME_FILE):
        print("No game found. Installing latest version...")
        if exe_url and attempt_update(exe_url, hash_url):
            print(f"Installed version {latest_version}")
            set_local_version(latest_version)
        else:
            print("Installation failed. Exiting.")
            return

    elif latest_version != local_version:
        print(f"New version available: {latest_version}")
        if exe_url and attempt_update(exe_url, hash_url):
            print(f"Updated to {latest_version}")
            set_local_version(latest_version)
        else:
            print("Update failed. Proceeding with current version...")

    else:
        print("You are on the latest version.")

    launch_game()

if __name__ == "__main__":
    main()
