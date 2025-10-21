import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

def search_web(query, num_results=5):
    """Use SerpAPI to get top URLs for the given query."""
    params = {
        "q": query,
        "api_key": os.getenv("SERPAPI_KEY"),
        "num": num_results,
        "hl": "en"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    urls = []

    for item in results.get("organic_results", []):
        link = item.get("link")
        if link and link not in urls:
            urls.append(link)

    return urls[:num_results]


if __name__ == "__main__":
    q = input("Enter query: ")
    print(search_web(q))
