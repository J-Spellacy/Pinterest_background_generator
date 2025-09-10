import os
import requests
from bs4 import BeautifulSoup
import re

## please note this was generated mostly with chatgpt 5.0

# file paths
HTML_FILE = "/home/jude/Documents/pinterest.html"
OUTPUT_DIR = "/home/jude/Pictures/pint_pins"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# open html file as read and parse for links
with open(HTML_FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")
pin_links = [a["href"] for a in soup.find_all("a", href=True) if "/pin/" in a["href"]]
print(f"Found {len(pin_links)} pins")

# Scrape each pin page for the actual image
for i, link in enumerate(pin_links, 1):
    try:
        r = requests.get(link, timeout=10)
        r.raise_for_status()
        pin_soup = BeautifulSoup(r.text, "html.parser")

        # Pinterest puts the main image in <meta property="og:image">
        meta = pin_soup.find("meta", property="og:image")
        if not meta:
            print(f"No image found for {link}")
            continue

        img_url = meta["content"]
        ext = os.path.splitext(img_url.split("?")[0])[1] or ".jpg"
        filename = os.path.join(OUTPUT_DIR, f"pin_{i}{ext}")

        img_data = requests.get(img_url, timeout=10).content
        with open(filename, "wb") as f:
            f.write(img_data)

        print(f"Downloaded {filename}")

    except Exception as e:
        print(f"Failed {link}: {e}")