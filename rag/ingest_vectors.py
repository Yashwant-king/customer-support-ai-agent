import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text

from rag.chunk_documents import create_chunks
from rag.load_documents import load_documents


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env")

engine = create_engine(DATABASE_URL)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    # 1. Load documents
    documents = load_documents()

    # 2. Create chunks
    chunks = create_chunks(documents)

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    # 3. Load embedding model
    model = SentenceTransformer(MODEL_NAME)

    # 4. Extract chunk text
    texts = [chunk["content"] for chunk in chunks]

    # 5. Generate embeddings
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
    )

    # 6. Insert into PostgreSQL
    with engine.begin() as connection:

        # Clear previous ingestion
        connection.execute(
            text("TRUNCATE TABLE knowledge_chunks")
        )

        for chunk, embedding in zip(chunks, embeddings):

            embedding_string = "[" + ",".join(
                str(float(value)) for value in embedding
            ) + "]"

            connection.execute(
                text("""
                    INSERT INTO knowledge_chunks
                    (content, source, chunk_id, embedding)
                    VALUES
                    (:content, :source, :chunk_id, CAST(:embedding AS vector))
                """),
                {
                    "content": chunk["content"],
                    "source": chunk["source"],
                    "chunk_id": chunk["chunk_id"],
                    "embedding": embedding_string,
                },
            )

    print("\nIngestion completed successfully.")


if __name__ == "__main__":
    main()