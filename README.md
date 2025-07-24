# README.md
readme = '''
# HerbScholar 🌿

**HerbScholar** is a free, open-source project that extracts and indexes PubMed articles related to herbal medicine. It provides a simple search interface to explore these articles directly in your browser — no server or backend needed.

---

## 🔍 Features
- Automatically downloads and filters PubMed MEDLINE data
- Searches for articles with MeSH terms: `Phytotherapy`, `Plants, Medicinal`, `Herbal Medicine`
- Uses [Lunr.js](https://lunrjs.com) for client-side, instant search
- Updates itself monthly via GitHub Actions

---

## 📦 Repo Contents

- `parser.py` – Python script to download, filter, and build the index
- `filtered_articles.json` – Filtered data output
- `search_index.json` – Lunr.js-ready index
- `index.html` – Static frontend for search (works with GitHub Pages!)
- `.github/workflows/update.yml` – GitHub Actions automation

---

## 🛠 How It Works

1. `parser.py` downloads one MEDLINE baseline file from NCBI
2. It keeps only articles tagged with herbal medicine MeSH terms
3. It creates two JSON files:
   - `filtered_articles.json` – full article metadata
   - `search_index.json` – indexed for Lunr.js
4. GitHub Actions runs this script monthly and pushes updated results

---

## 🌐 Hosting with GitHub Pages

To publish your search tool online:
1. Go to your GitHub repo → **Settings** → **Pages**
2. Choose branch: `main`, folder: `/root`
3. Click **Save** → Your HerbScholar site will be live!

---

## 📅 Automation Schedule
This repo updates automatically on the 1st of each month.
You can also trigger it manually from the **Actions** tab.

---

## 🙌 Credits
- PubMed data from [NCBI](https://www.ncbi.nlm.nih.gov/pubmed/)
- Indexing with [Lunr.js](https://lunrjs.com)
- Built entirely on free tools — no servers, no APIs, no databases

'''

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)
