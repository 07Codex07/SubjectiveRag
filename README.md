# Subjective RAG System 🧠📈
### Ask anything about stocks. Get answers that are evidence-backed, verified, and auditable.

A next-generation subjectivity-aware RAG pipeline built for investment-style questions like "Should I buy HDFC Bank stock right now?" or "Is Tesla a good long-term investment?" — with multi-layer verification so the answer is never just vibes.

---

## 🚀 Features

- 🔍 **SERP-powered web search** — fetches top results via SerpAPI
- 🌐 **Robust scraping** — handles HTML, PDF, JS-rendered pages, and Cloudflare-protected sites
- 📄 **BM25 ranking** — chunks and ranks evidence for relevance
- 🤖 **Worker LLM** — generates analysis with claim-level source attribution
- ✅ **Checker LLM** — validates logical consistency and flags fabricated facts
- 🛡️ **Deterministic claim verifier** — rule-based (non-LLM) check that each claim exists verbatim in sources
- 📜 **Full query logging** — every run is auditable as a `.jsonl` file

---

## 🔄 Pipeline

Query → Classification → Web Search → Scraping → Chunking + BM25 → Worker LLM → Checker LLM → Claim Verifier → Final Answer

1. **Query Classification** — routes to finance, crypto, news, or general domain
2. **Web Search** — SerpAPI fetches up to 8 URLs, filtered by whitelisted domains
3. **Scraping** — multi-strategy scraper with caching, PDF support, and Yahoo Finance auto-extraction
4. **Chunking + BM25** — deduped chunks ranked by relevance; top 5 selected as evidence
5. **Worker LLM** — produces final answer + claim list with evidence snippets and source URLs
6. **Checker LLM** — ensures no fabricated facts, checks source-claim alignment
7. **Deterministic Verifier** — non-LLM rule-based check; computes claim_precision and hallucination_rate
8. **Final Output** — worker answer shown only if checker = VALID and claim_precision ≥ 0.9, else safe fallback with mismatch report

---

## ⚙️ Setup

git clone <your-repo-url>
cd submission/
pip install -r requirements.txt
python scripts/run_subjective_rag.py "should I buy HDFC Bank stock now?"

---

## 📁 Project Structure

<img width="384" height="637" alt="image" src="https://github.com/user-attachments/assets/110e3760-0040-4de6-a91a-6b5997ead09d" />

---

## 🛡️ Verification Logic

Final answer is shown only when ALL conditions are met:
- Checker LLM returns VALID
- claim_precision ≥ 0.9

Otherwise, a safe fallback is returned with:
- Worker answer
- Verifier notes
- Claim-evidence mismatch report

---

## 📊 Output Metrics

- claim_precision
- hallucination_rate
- valid_claims / total_claims

---

## 🔭 Future Extensions

- Real-time price feeds
- Sentiment scoring
- Multi-agent analysis
- Vector DB for historical queries
- Dashboard visualization
- Playbook templates per industry

---

Built by Vinayak
