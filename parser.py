# parser.py

import requests
from bs4 import BeautifulSoup
import re

BASELINE_URL = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"

response = requests.get(BASELINE_URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

files = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if re.match(r'^pubmed24n\d{4}\.xml\.gz$', href):
        files.append(href)

if not files:
    raise Exception("No baseline files found")

latest_file = sorted(files)[-1]
download_url = BASELINE_URL + latest_file

print("Latest baseline file:", latest_file)
print("Download URL:", download_url)


import requests
import gzip
import xml.etree.ElementTree as ET
import json
from io import BytesIO

HERBAL_TERMS = {"Phytotherapy", "Plants, Medicinal", "Herbal Medicine"}



def download_baseline_file():
    print("Downloading baseline file...")
    response = requests.get(download_url)
    response.raise_for_status()
    return BytesIO(response.content)


def iter_herbal_articles(fileobj):
    articles = []
    context = ET.iterparse(gzip.GzipFile(fileobj=fileobj), events=("end",))
    for event, elem in context:
        if elem.tag == "PubmedArticle":
            mesh_terms = [mh.findtext("DescriptorName") for mh in elem.findall(".//MeshHeading") if mh.find("DescriptorName") is not None]
            if not any(term in HERBAL_TERMS for term in mesh_terms):
                elem.clear()
                continue

            title = elem.findtext(".//ArticleTitle") or ""
            abstract = elem.findtext(".//Abstract/AbstractText") or ""
            articles.append({
                "title": title.strip(),
                "abstract": abstract.strip(),
                "mesh_terms": mesh_terms
            })
            elem.clear()
    return articles


def save_filtered_data(articles):
    with open("filtered_articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)


def save_lunr_index(articles):
    lunr_index = {
        "version": "0.9.5",
        "fields": ["title", "abstract"],
        "ref": "id",
        "documents": [
            {"id": i, "title": a["title"], "abstract": a["abstract"]} for i, a in enumerate(articles)
        ]
    }
    with open("search_index.json", "w", encoding="utf-8") as f:
        json.dump(lunr_index, f, ensure_ascii=False)


def main():
    fileobj = download_baseline_file()
    articles = iter_herbal_articles(fileobj)
    print(f"Found {len(articles)} herbal-related articles.")
    save_filtered_data(articles)
    save_lunr_index(articles)


if __name__ == "__main__":
    main()
