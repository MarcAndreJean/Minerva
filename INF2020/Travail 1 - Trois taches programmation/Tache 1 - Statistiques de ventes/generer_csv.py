"""Generate sales.csv : 1 000 000 entries."""
import csv
import random
from pathlib import Path

NUMBER_OF_LINES = 1_000_000
CATEGORIES = ["food", "books", "electronic", "clothing", "garden"]

random.seed(42)
path = Path(__file__).parent / "sales.csv"

with open(path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "category", "amount", "quantity"])
    for i in range(1, NUMBER_OF_LINES + 1):
        writer.writerow([
            i,
            random.choice(CATEGORIES),
            f"{random.uniform(1, 500):.2f}",  # amount in dollars, 2 decimal places
            random.randint(1, 20),
        ])

print(f"{NUMBER_OF_LINES} lines written to {path}")
