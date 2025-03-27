import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import os
import time
import subprocess

# === CONFIG ===
BASE_URL = "https://cloud.google.com/marketplace/docs/"
DOMAIN = "cloud.google.com"
MAX_DEPTH = 2
OUTPUT_DIR = "output"
OUTPUT_FILE = "gcp_marketplace_links.txt"

# === GLOBALS ===
visited = set()
found_links = []

def clean_url(url):
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

def crawl(url, depth=0):
    url = clean_url(url)
    if depth > MAX_DEPTH or url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Skipping {url} (status {response.status_code})")
            return
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup.find_all("a", href=True):
        href = tag['href']
        if any(ext in href for ext in ['.pdf', '.jpg', '.png', '.gif', '.svg', '#']):
            continue
        full_url = urljoin(url, href)
        cleaned = clean_url(full_url)
        if DOMAIN in urlparse(cleaned).netloc and cleaned not in visited:
            found_links.append(cleaned)
            print(f"[{len(found_links)}] {cleaned}")

            crawl(cleaned, depth + 1)
            time.sleep(0.2)

# === START ===
print(f"Starting crawl from: {BASE_URL}")
crawl(BASE_URL)

# === SAVE TO FILE ===
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

with open(output_path, "w", encoding="utf-8") as f:
    for link in sorted(set(found_links)):
        f.write(link + "\n")

print(f"\n✅ Done. {len(found_links)} links saved to {output_path}")

# === GIT COMMIT & PUSH ===
try:
    subprocess.run(["git", "add", output_path], check=True)
    subprocess.run(["git", "commit", "-m", "Update GCP Marketplace links"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("🚀 File committed and pushed to GitHub!")
except subprocess.CalledProcessError as e:
    print(f"❌ Git operation failed: {e}")
