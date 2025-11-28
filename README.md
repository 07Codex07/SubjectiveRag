# README – Subjective RAG System

## 📌 Overview

This project implements a next-generation subjectivity-aware RAG pipeline designed to answer investment-style questions such as:

- "Should I buy HDFC Bank stock right now?"
- "Is Tesla a good long-term investment?"

The system performs:
- SERP-powered web search  
- Robust scraping (HTML/PDF/images/JS-rendered pages)  
- Chunking + BM25 ranking  
- Worker LLM analysis generation  
- Checker LLM consistency verification  
- Deterministic claim verification against sources  
- Automatic logging of each query

This ensures answers are objective, auditable, and evidence-backed.

---

## 📂 Project Structure

<img width="384" height="637" alt="image" src="https://github.com/user-attachments/assets/110e3760-0040-4de6-a91a-6b5997ead09d" />



---

## 🔍 1. Web Search Layer (`web_search.py`)

Uses SerpAPI to fetch top Google results.

Features:
- Extracts organic results
- Removes duplicates
- Returns top N URLs based on search query

Usage:

urls = search_web("should I buy Tata Motors stock?", num_results=8)


🌐 3. Fetching & Scraping Layer (fetch_and_scrape.py)

Primary scraper used by the RAG pipeline.

Capabilities:

Cloudflare/bot bypass with cloudscraper

Random delays + User-Agent rotation

Local caching for speed

Visible HTML text extraction

PDF extraction

Newspaper3k fallback

Financial table extraction

Automatic Yahoo Finance scraping (Market cap, PE ratio, revenue growth, EBITDA margin, financial statements)

Flow:

Check cache

Requests + cloudscraper

Detect PDF and extract

Extract tables + text

Fallback to newspaper3k

Save cleaned text in cache

🌐 3. Universal Scraper (universal_scraper.py)

 A heavy-duty scraper with multiple fallbacks.

Fetching strategies:

requests

cloudscraper

Playwright (headless browser for JS-rendered content)

Extraction capabilities:

Metadata extraction

Text extraction

Images + OCR (Tesseract)

Tables via Pandas

PDF extraction via pdfplumber

JSON-LD extraction

Chart/config extraction from scripts

XHR API capture in Playwright

Outputs:
{
"url": "",
"raw_html": "",
"text": "",
"metadata": {},
"tables": [],
"images": [],
"charts": [],
"captured_xhr": []
}

🧠 4. Orchestrator Pipeline (run_subjective_rag.py)

Run using:
python scripts/run_subjective_rag.py "should I buy HDFC Bank stock now?"

Pipeline Steps:

Query Classification
Routes queries based on detected domain:

finance

crypto

news

general

Web Search
Uses SerpAPI → fetches up to 8 URLs → filters by whitelisted domains.

Scraping
Uses fetch_and_scrape to scrape each URL.

Chunking + BM25 Ranking

Splits text into chunks

Dedupes

Ranks using BM25

Selects top 5 chunks as evidence

Worker LLM (analysis generator)
Outputs:

Final answer

List of claims with:

claim text

evidence snippet

source URL

Checker LLM (validation agent)
Ensures:

Logical consistency

No fabricated facts

Sources match claims

Deterministic Claim Verification
Independent rule-based system (non-LLM):

Checks if each claim exists verbatim in sources

Flags missing or hallucinated claims

Scoring

claim_precision

hallucination_rate

Final Output Logic
If:

checker says VALID

claim_precision ≥ 0.9

Then:
final_answer = worker answer

Else (safe fallback):

worker answer

verifier notes

claim evidence mismatch report

Logging
Stored in:
data/logs/log_<timestamp>.jsonl

🛡️ 5. Deterministic Claim Verifier (claim_verifier.py)

Checks claims from Worker LLM against scraped sources.

Process:

Normalize all text

Search for exact claim string in scraped data

Mark as VALID or INVALID

Create evidence excerpts

Compute metrics

Outputs:

verification list

metrics

claim_precision

hallucination_rate

valid_claims

total_claims

📊 Evidence Tracking

Each source is formatted as:

SOURCE_URL: ...
SOURCE_TEXT:
...extracted content...
<<END_SOURCE>>

Both Worker and Checker LLMs receive these identical evidence blocks.

🗄️ Caching System

All scraped pages are cached in:
data/cache/

Prevents repeated scraping and reduces latency.

📜 Logging System

Logs include:

query

URLs

top chunks

worker output

checker output

deterministic verification

scoring

Stored as .jsonl files for auditing.

🚀 Running the System

python scripts/run_subjective_rag.py "should I buy Infosys stock?"

Outputs:

Classification

URLs used

Scraper logs

Ranked chunks

Worker answer

Checker evaluation

Verification metrics

Final answer

📌 Future Extensions

Possible upgrades:

Real-time price feeds

Sentiment scoring

Multi-agent analysis

Vector DB for historical queries

Dashboard visualization

Playbook templates per industry

👤 Author

Vinayak — AI/ML Engineer
