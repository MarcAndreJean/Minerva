"""sales_stats_from_csv.py (Task 1)
============
Output statistics (mean, median, min, max) from a CSV file.
Csv file must have a header with at least the columns "price" and "quantity".

Usage :
    python sales_stats_from_csv.py <sales.csv>
"""

import csv
import statistics
import sys
import time

PRICE_COLUMN = "price"
QUANTITY_COLUMN = "quantity"


def main(csv_path) -> None:
    """Output statistics (mean, median, min, max) from a CSV file.

    Args:
        csv_path: CSV filepath with columns "price" and "quantity".
    """
    # Start measuring time (performance counter).
    perf_start_time = time.perf_counter() 

    # Load data from CSV file.
    price_list = []
    quantity_list = []
    try:
        with open(csv_path, encoding="utf-8") as file:
            csv_data = csv.DictReader(file)
            for line in csv_data:
                price_list.append(float(line[PRICE_COLUMN]))
                quantity_list.append(int(line[QUANTITY_COLUMN]))
    except (KeyError, ValueError) as e:
        print(f"Error while parsing file '{csv_path}': {e}")
        return

    # Print statistics for price and quantity.
    print("Price statistics:")
    printStatsFromList(price_list)

    print("Quantity statistics:")
    printStatsFromList(quantity_list)

    perf_time = time.perf_counter() - perf_start_time
    print(f"Execution time = {perf_time:.3f}s")


def printStatsFromList(list) -> None:
    """Print statistics (mean, median, min, max) from a list of values.

    Args:
        list: A list of numeric values.
    """
    print(f"\tMean:\t{statistics.mean(list):.2f}")
    print(f"\tMedian:\t{statistics.median(list):.2f}")
    print(f"\tMin:\t{min(list):.2f}")
    print(f"\tMax:\t{max(list):.2f}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Missing CSV file path argument.")
        sys.exit(1)
    main(sys.argv[1])
