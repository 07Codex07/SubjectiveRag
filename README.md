# 🧠 SubjectiveRAG — AI-Driven Financial Research Assistant  
*Built by Vinayak · Powered by Groq, SerpAPI & CloudScraper*

---

## 🌍 Overview

**SubjectiveRAG** is an AI-powered **financial research and analysis pipeline** that automatically searches the web for the latest company financials, extracts clean text from multiple data sources, and produces a **human-style research report** — just like a professional stock analyst.

The project blends **Retrieval-Augmented Generation (RAG)** with intelligent web scraping, using tools like **SerpAPI, CloudScraper, BeautifulSoup, and LangChain**.  
You can ask it about **valuation ratios (P/E, P/B, EPS Growth, etc.)**, **analyst upgrades/downgrades**, or even **financial surprises** for any listed company, and it will give you a structured, explainable summary.

---

## 💡 What Makes SubjectiveRAG Special

✅ **Human-style financial commentary** — reports read like an analyst wrote them  
✅ **Real-time data retrieval** — uses SerpAPI and scrapers to get the freshest info  
✅ **Cleans & caches data** — smart caching to avoid refetching pages  
✅ **Automatic retry and Cloudflare bypass** — powered by CloudScraper  
✅ **PDF + HTML + Newspaper3k fallback** — handles most financial document formats  
✅ **Modular RAG pipeline** — plug in your favorite LLM or retriever easily  

---

## 🧱 Folder Structure


<img width="755" height="612" alt="image" src="https://github.com/user-attachments/assets/698934b0-50bb-4d22-9616-c0423a1601d7" />


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/subjective_rag.git
cd subjective_rag
```

2️⃣ Create and Activate a Virtual Environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a file named .env in the project root with the following contents:

GROQ_API_KEY=your_groq_api_key_here
SERPAPI_KEY=your_serpapi_key_here
USER_AGENT=MyResearchBot/1.0 (contact: your_email@example.com)


💡 Tip:
You can get a free SerpAPI key at https://serpapi.com

🚀 Running SubjectiveRAG

Once installed and configured:

python -m scripts.run_subjective_rag


You’ll see:

Enter topic:


You can enter any query such as:

P/E & P/B Multiples, EPS / Revenue Growth, EBITDA Margin, Debt/EBITDA Ratio, Dividend Yield, Analyst Upgrade/Downgrade of Tata Motors


The system will:

1)Search the web using SerpAPIFetch 5–10 relevant pages
2)Fetch 5–10 relevant pages
3)Scrape text (with CloudScraper + fallback)
4)Store the cleaned text in data/cache/
5)Use BM25 / FAISS retrieval to chunk relevant info
6)Generate a full analyst-style report via Groq API

# Example Output

🔍 Searching web for: P/E & P/B Multiples, EPS / Revenue Growth, EBITDA Margin, Debt/EBITDA Ratio, Dividend Yield, Analyst Upgrade/Downgrade of Tata Motors

Found 5 sources.
Fetching and scraping...
...
🧠 Generating analysis...

**Tata Motors: A Comprehensive Analysis**

As a research analyst, I have gathered insights from various sources to provide a balanced analysis of Tata Motors...

**Key Strengths**
1. Reduced Debt
2. Good Profit Growth
3. Strong ROE
...

**Valuation Metrics**
- P/E Ratio: 6.89
- Price/Book: 1.26
- Debt/Equity: 0.23

**Conclusion**
Tata Motors is a well-established player in the automobile industry...

**Recommendation:** HOLD with potential upside of 15%.

# Example of .env file
```
GROQ_API_KEY=groq_xxx
SERPAPI_KEY=serpapi_xxx
USER_AGENT=MyResearchBot/1.0 (contact: vinayak@example.com)
```
