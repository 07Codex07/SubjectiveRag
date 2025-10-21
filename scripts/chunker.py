def chunk_text(text, max_length=300):
    """Split text into clean overlapping chunks."""
    words = text.split()
    chunks, step = [], max_length // 2

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + max_length])
        if chunk:
            chunks.append(chunk)
    return chunks


if __name__ == "__main__":
    sample = "This is a demo paragraph to test chunking function for subjective rag pipeline."
    print(chunk_text(sample))
