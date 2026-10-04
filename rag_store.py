from rag_chunks import load_and_chunk_documents
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")


def build_vector_store():
    chunks = load_and_chunk_documents()

    if not chunks:
        raise ValueError(
            "No documents found. Add a PDF to the documents folder first."
        )

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(texts)

    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])

    index.add(embeddings)

    return index, chunks


if __name__ == "__main__":
    index, chunks = build_vector_store()

    print("Vector store created successfully!")
    print("Total chunks:", len(chunks))
    print("Total vectors:", index.ntotal)
    print("Vector dimension:", index.d)