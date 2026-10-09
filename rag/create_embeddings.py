from sentence_transformers import SentenceTransformer

from rag.chunk_documents import create_chunks
from rag.load_documents import load_documents


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"



def main():
    # Load documents
    documents = load_documents()

    # Create chunks
    chunks = create_chunks(documents)

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    # Load embedding model
    model = SentenceTransformer(MODEL_NAME)

    # Extract text
    texts = [chunk["content"] for chunk in chunks]

    # Generate embeddings
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
    )

    print("\nEmbedding generation complete.")
    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Embedding dimension: {embeddings.shape[1]}")

    # Inspect first embedding
    print("\nFirst embedding:")
    print(embeddings[0][:10])


if __name__ == "__main__":
    main()