import requests
from bs4 import BeautifulSoup
import os

FEED_URL = "https://azure.microsoft.com/en-us/blog/feed/"
OUTPUT_DIR = "output"
OUTPUT_FILE = "azure_blog_articles.txt"

# Coleta o conteúdo do RSS feed
try:
    response = requests.get(FEED_URL, timeout=10)
    response.raise_for_status()
except Exception as e:
    print(f"❌ Error fetching RSS feed: {e}")
    exit()

# Faz o parsing XML
soup = BeautifulSoup(response.content, features="xml")
items = soup.find_all("item")

# Extrai os links dos artigos
article_links = [item.link.text for item in items]

# Salva no arquivo
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

with open(output_path, "w", encoding="utf-8") as f:
    for link in sorted(article_links):
        f.write(link + "\n")

print(f"\n✅ Done. {len(article_links)} article links saved to {output_path}")
