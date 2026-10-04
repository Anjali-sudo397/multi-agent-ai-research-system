from rag_store import build_vector_store
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve(query, k=3):
    index, chunks = build_vector_store()

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    k = min(k, index.ntotal)
    distances, indices = index.search(query_embedding, k)

    results = []

    for i in indices[0]:
        if i < len(chunks):
            results.append(chunks[i])

    return results


if __name__ == "__main__":
    query = input("Ask something about the documents: ")

    results = retrieve(query)

    print("\nRelevant chunks:\n")

    for i, result in enumerate(results, 1):
        print("=" * 60)
        print(f"RESULT {i}")
        print("SOURCE:", result["source"])
        print("=" * 60)
        print(result["text"])