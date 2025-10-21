"""
scripts/fetch_and_scrape.py

Human-friendly, resilient web fetcher for the subjective_rag project.

Features:
- Cloudflare/bot bypass using cloudscraper
- Realistic user-agent rotation
- Smart retry/backoff with random delays
- Local caching (data/cache/)
- PDF and newspaper3k fallback support
- Clear, conversational logging

Author: Vinayak
"""

import os
import time
import random
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Optional imports
try:
    import cloudscraper
    HAS_CLOUDSCRAPER = True
except Exception:
    HAS_CLOUDSCRAPER = False

try:
    from newspaper import Article
    HAS_NEWSPAPER = True
except Exception:
    HAS_NEWSPAPER = False

try:
    from io import BytesIO
    from PyPDF2 import PdfReader
    HAS_PDF = True
except Exception:
    HAS_PDF = False

load_dotenv()

# Cache directory
CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
]

BASE_HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
}


def _get_cache_path(url: str) -> Path:
    return CACHE_DIR / (hashlib.md5(url.encode("utf-8")).hexdigest() + ".txt")


def _cache_text(path: Path, text: str) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"[Warn] Failed to cache text: {e}")


def _extract_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "form", "aside", "svg"]):
        tag.decompose()
    return " ".join(soup.get_text(separator=" ").split())


def _extract_text_from_pdf(content: bytes) -> str:
    if not HAS_PDF:
        return ""
    try:
        reader = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except Exception as e:
        print(f"[Warn] PDF extraction failed: {e}")
        return ""


def _fallback_newspaper(url: str) -> str:
    if not HAS_NEWSPAPER:
        return ""
    try:
        a = Article(url)
        a.download()
        a.parse()
        return (a.title + "\n\n" + a.text).strip()
    except Exception:
        return ""


def _fetch_raw(url: str, headers: dict, timeout: int = 20):
    import requests

    # Yahoo Finance bypass via SerpAPI
    if "finance.yahoo.com" in url:
        serpapi_key = os.getenv("SERPAPI_KEY")
        if serpapi_key:
            try:
                print("[Bypass] Using SerpAPI for Yahoo Finance…")
                params = {"engine": "google", "q": url, "api_key": serpapi_key}
                r = requests.get("https://serpapi.com/search", params=params, timeout=timeout)
                r.raise_for_status()
                data = r.json()
                text = " ".join(res.get("snippet", "") for res in data.get("organic_results", []))
                return type("FakeResp", (), {"status_code": 200, "text": text, "headers": {"Content-Type": "text/html"}})()
            except Exception as e:
                print(f"[SerpAPI failed] {e}")

    # Normal fetch
    if HAS_CLOUDSCRAPER:
        try:
            scraper = cloudscraper.create_scraper(
                browser={
                    "browser": random.choice(["chrome", "firefox"]),
                    "platform": random.choice(["windows", "linux"]),
                    "mobile": False,
                }
            )
            headers["Cookie"] = f"id={random.randint(100000,999999)}"
            return scraper.get(url, headers=headers, timeout=timeout)
        except Exception as e:
            print(f"[Info] cloudscraper failed: {e}")

    # Final fallback
    return requests.get(url, headers=headers, timeout=timeout)


def fetch_and_scrape(url: str, max_retries: int = 3, min_delay: float = 1.5, max_delay: float = 4.0) -> str:
    """Main web fetcher. Handles retries, caching, and fallbacks."""

    cache_path = _get_cache_path(url)
    if cache_path.exists():
        print(f"[Cache] Loaded cached copy for: {url}")
        try:
            return cache_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[Warn] Cache read failed: {e}")

    for attempt in range(1, max_retries + 1):
        ua = os.getenv("USER_AGENT") or random.choice(USER_AGENTS)
        headers = {**BASE_HEADERS, "User-Agent": ua}

        delay = random.uniform(min_delay, max_delay)
        print(f"[{attempt}/{max_retries}] Visiting: {url}  (sleep {delay:.1f}s, UA: {ua.split(' ')[0]})")
        time.sleep(delay)

        try:
            resp = _fetch_raw(url, headers=headers, timeout=20)
            if not resp or getattr(resp, "status_code", 500) >= 400:
                raise RuntimeError(f"Bad response ({getattr(resp, 'status_code', 'None')})")

            ctype = (resp.headers.get("Content-Type", "").lower() if hasattr(resp, "headers") else "")
            text = _extract_text_from_pdf(resp.content) if "pdf" in ctype else _extract_text_from_html(resp.text)

            if not text.strip():
                print("[Info] Empty extraction — trying newspaper3k fallback…")
                text = _fallback_newspaper(url)

            if text.strip():
                _cache_text(cache_path, text)
                print(f"[OK] Scraped: {url}")
                return text

            raise RuntimeError("No usable text extracted")

        except Exception as e:
            backoff = random.uniform(2.5, 6.0) * attempt
            print(f"[Warn] Attempt {attempt} failed: {e}. Waiting {backoff:.1f}s before retry.")
            time.sleep(backoff)

    print(f"[Error] All attempts failed for {url}")
    last_try = _fallback_newspaper(url)
    if last_try:
        print("[OK] Using newspaper3k fallback.")
        _cache_text(cache_path, last_try)
        return last_try

    return ""


if __name__ == "__main__":
    url = input("Enter URL: ").strip()
    text = fetch_and_scrape(url)
    print("\n--- Preview ---\n")
    print(text[:1000] if text else "[No text extracted]")
