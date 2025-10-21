from rank_bm25 import BM25Okapi

def rank_chunks(chunks, query, top_n=5):
    """Return top-N relevant chunks using BM25 ranking."""
    tokenized = [chunk.split() for chunk in chunks]
    bm25 = BM25Okapi(tokenized)
    scores = bm25.get_scores(query.split())
    ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)
    return [c for c, _ in ranked[:top_n]]


if __name__ == "__main__":
    docs = ["AI is transforming healthcare", "ML models require data", "Python is popular"]
    print(rank_chunks(docs, "AI healthcare"))
