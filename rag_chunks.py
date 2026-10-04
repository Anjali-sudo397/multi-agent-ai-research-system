from rag_ingest import load_documents


def create_chunks(text, chunk_size=800, overlap=150):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def load_and_chunk_documents():
    documents = load_documents()

    all_chunks = []

    for document in documents:
        chunks = create_chunks(document["text"])

        for chunk in chunks:
            all_chunks.append({
                "source": document["source"],
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":
    chunks = load_and_chunk_documents()

    print("Total chunks:", len(chunks))

    for i, chunk in enumerate(chunks[:3], 1):
        print("\n" + "=" * 60)
        print("CHUNK", i)
        print("SOURCE:", chunk["source"])
        print("=" * 60)
        print(chunk["text"])