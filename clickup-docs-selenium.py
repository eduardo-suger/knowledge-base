from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, urlunparse
import os
import time
import subprocess

# === CONFIG ===
BASE_URL = "https://doc.clickup.com/42081486/d/h/18476e-4831/4260048a22284ea/18476e-6791"
DOMAIN = "doc.clickup.com"
OUTPUT_DIR = "output"
OUTPUT_FILE = "clickup_links_selenium.txt"

# === HEADLESS SELENIUM SETUP ===
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

print(f"🔍 Accessing: {BASE_URL}")
driver.get(BASE_URL)
time.sleep(5)  # esperar o conteúdo carregar

# === EXTRACT LINKS ===
links = driver.find_elements(By.TAG_NAME, "a")
found_links = []

for link in links:
    href = link.get_attribute("href")
    if href and DOMAIN in href:
        found_links.append(href)

driver.quit()

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
    subprocess.run(["git", "commit", "-m", "Update ClickUp links via Selenium"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("🚀 File committed and pushed to GitHub!")
except subprocess.CalledProcessError as e:
    print(f"❌ Git operation failed: {e}")
