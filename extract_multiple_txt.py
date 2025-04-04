import requests
from bs4 import BeautifulSoup
import os
import re

# Caminhos
links_file = "output/suger_doc_links.txt"
output_folder = "extracted_pages"

# Cria a pasta de saída se não existir
os.makedirs(output_folder, exist_ok=True)

# Função para criar nomes de arquivos válidos com base na URL
def sanitize_filename(url):
    filename = url.replace("https://", "").replace("http://", "")
    filename = re.sub(r'[^\w\-_.]', '_', filename)
    return filename[:100] + ".txt"  # Limita tamanho se for muito grande

# Função para extrair texto da URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        for tag in soup(['script', 'style', 'noscript']):
            tag.decompose()

        text = soup.get_text(separator='\n')
        lines = [line.strip() for line in text.splitlines()]
        clean_text = "\n".join(line for line in lines if line)

        return clean_text
    except Exception as e:
        print(f"❌ Error extracting {url}: {e}")
        return None

# Lê os links do arquivo
with open(links_file, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

# Processa cada link
for url in urls:
    print(f"🔍 Processing: {url}")
    content = extract_text_from_url(url)
    if content:
        filename = sanitize_filename(url)
        output_path = os.path.join(output_folder, filename)
        with open(output_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(content)
        print(f"✅ Saved to {output_path}")
    else:
        print(f"⚠️ Skipped: {url}")
