"""prime-numbers.py (Task 2)
============
Output list of prime numbers up to a given limit.
Implementation of the `Sieve of Eratosthenes` algorithm.

Usage :
    python prime-numbers.py <limit>
"""

import math
import sys
import time


def main(n) -> None:
    """Output list of prime numbers up to a given limit.

    Args:
        n: The upper limit (inclusive) for generating prime numbers.
    """
    try:
        n = int(n)
    except ValueError:
        print("Error: Please provide an integer greater than 1.")
        return

    if n < 2:
        print("Error: Please provide an integer greater than 1.")
        return

    # Start measuring time (performance counter)
    perf_start_time = time.perf_counter()

    is_prime_list = [True] * (n + 1)
    is_prime_list[0] = is_prime_list[1] = False

    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime_list[i]:
            # We eleminate multiples of `i`.
            for j in range(i * i, n + 1, i):
                is_prime_list[j] = False

    # Print the list of prime numbers.
    primes = [i for i, is_prime in enumerate(is_prime_list) if is_prime]
    print(f"Prime numbers up to {n}:")
    print(", ".join(map(str, primes)))

    perf_time = (time.perf_counter() - perf_start_time) * 1000
    print(f"Execution time = {perf_time:.2f} ms")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Missing limit argument.")
        sys.exit(1)
    main(sys.argv[1])
