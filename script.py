import hashlib

file_path = "dist/main.exe"

sha256 = hashlib.sha256()
with open(file_path, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        sha256.update(chunk)

hash_value = sha256.hexdigest()
print("SHA-256:", hash_value)

with open("release_assets/main.sha256", "w") as f:
    f.write(hash_value)
