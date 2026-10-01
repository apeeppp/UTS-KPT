import random
import string
from pathlib import Path

NIM = 247006111162
TOTAL_DATA = 1620

OUTPUT_DIR = Path("dataset")


def generate_text(length=4000):
    words = [
        "parallel",
        "computing",
        "distributed",
        "system",
        "thread",
        "process",
        "python",
        "data",
        "analysis",
        "algorithm"
    ]

    chars = string.ascii_letters + string.digits + " !@#$%^&*()"

    parts = []

    for _ in range(length // 20):
        parts.append(random.choice(words))

        for _ in range(5):
            parts.append(random.choice(chars))

    return " ".join(parts)


def main():
    random.seed(NIM)

    OUTPUT_DIR.mkdir(exist_ok=True)

    for i in range(1, TOTAL_DATA + 1):
        file_path = OUTPUT_DIR / f"data_{i:04d}.txt"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(generate_text())

    print(f"Dataset berhasil dibuat: {TOTAL_DATA} file")
    print(f"Seed: {NIM}")
    print(f"Lokasi: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()