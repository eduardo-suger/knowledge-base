import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import os

# === CONFIG ===
BASE_URL = "https://learn.microsoft.com/en-us/partner-center/"
DOMAIN = "learn.microsoft.com"
PATH_PREFIX = "/en-us/partner-center"
OUTPUT_DIR = "output"
OUTPUT_FILE = "azure_partnercenter_doc_links.txt"
MAX_DEPTH = 2

visited = set()
found_links = []

def clean_url(url):
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

def crawl(url, depth=0):
    url = clean_url(url)
    if url in visited or depth > MAX_DEPTH:
        return
    visited.add(url)

    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            print(f"Skipping {url} (status {res.status_code})")
            return
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        return

    soup = BeautifulSoup(res.text, "html.parser")
    for tag in soup.find_all("a", href=True):
        href = tag['href']
        if any(ext in href for ext in ['.pdf', '.png', '.jpg', '.svg', '.gif', '#']):
            continue
        full_url = urljoin(url, href)
        cleaned = clean_url(full_url)
        parsed = urlparse(cleaned)

        if DOMAIN in parsed.netloc and parsed.path.startswith(PATH_PREFIX) and cleaned not in visited:
            found_links.append(cleaned)
            print(f"[{len(found_links)}] {cleaned}")
            crawl(cleaned, depth + 1)

# === RUN ===
print(f"🚀 Starting crawl from: {BASE_URL}")
crawl(BASE_URL)

# === SAVE TO FILE ===
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

valid_links = [link for link in visited if link.startswith(BASE_URL)]

with open(output_path, "w", encoding="utf-8") as f:
    for link in sorted(valid_links):
        f.write(link + "\n")

print(f"\n✅ Done. {len(valid_links)} links saved to {output_path}")
