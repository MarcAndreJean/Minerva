"""scraping.py (Task 3)
============
Scrape text content from a webpage.
Requirements:
    pip install beautifulsoup4

Usage:
    python scraping.py <url>

Example:
    python scraping.py https://www.scrapethissite.com/pages/
"""

import sys
import time
from urllib.request import HTTPError, Request, URLError, urlopen

from bs4 import BeautifulSoup


def main(url) -> None:
    """Scrape text content from a webpage.

    Args:
        url: The URL of the webpage to scrape.
    """
    print("url:", url)
    # Start measuring time (performance counter).
    perf_start_time = time.perf_counter()
    try:
        request = Request(url, headers={"User-Agent": "scraping/1.0"})
        html = urlopen(request).read().decode("utf-8")
    except (URLError, HTTPError) as e:
        print(f"Error while fetching URL '{url}': {e}")
        return

    soup = BeautifulSoup(html, "html.parser")

    # Remove content that isn't normally visible to the user.
    for element in soup(["script", "style", "noscript", "template"]):
        element.decompose()

    text = soup.get_text(separator=" ", strip=True)
    print("Word count:", len(text.split()))

    perf_time = time.perf_counter() - perf_start_time
    print(f"Execution time = {perf_time:.3f}s")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Missing URL argument.")
        sys.exit(1)
    main(sys.argv[1])
