import sys
from scripts.web_search import search_web
from scripts.fetch_and_scrape import fetch_and_scrape
from scripts.chunker import chunk_text
from scripts.bm25_indexer import rank_chunks
from scripts.llm_client import generate_subjective_analysis
from tqdm import tqdm

def run_subjective_analysis(query):
    print(f"\n🔍 Searching web for: {query}")
    urls = search_web(query)
    print(f"Found {len(urls)} sources\n")

    all_chunks = []
    for url in tqdm(urls, desc="Fetching pages"):
        text = fetch_and_scrape(url)
        if text:
            all_chunks.extend(chunk_text(text))

    print(f"\nTotal chunks: {len(all_chunks)}")

    top_chunks = rank_chunks(all_chunks, query, top_n=8)
    print("\n🧠 Generating analysis...\n")

    result = generate_subjective_analysis(query, top_chunks)
    print(result)


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or input("Enter topic: ")
    run_subjective_analysis(q)
