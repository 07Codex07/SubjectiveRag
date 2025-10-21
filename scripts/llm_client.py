import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_subjective_analysis(query, relevant_chunks):
    """Use LLM to write subjective analysis based on retrieved data."""
    context = "\n\n".join(relevant_chunks)
    prompt = f"""You are a research analyst.
Below is context gathered from multiple web sources about the topic: '{query}'.

Write a subjective, balanced analysis in a natural tone — as if you’re an expert human summarizing opinions and interpretations.

Context:
{context}

---
Answer:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
