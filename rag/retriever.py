import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env")

engine = create_engine(DATABASE_URL)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def retrieve(query: str, k: int = 3):
    # Convert the user's question into an embedding
    query_embedding = model.encode(query)

    embedding_string = "[" + ",".join(
        str(float(value)) for value in query_embedding
    ) + "]"

    sql = text("""
        SELECT
            content,
            source,
            chunk_id,
            1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
        FROM knowledge_chunks
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :k
    """)

    with engine.connect() as connection:
        results = connection.execute(
            sql,
            {
                "embedding": embedding_string,
                "k": k,
            },
        ).fetchall()

    return results


def main():
    query = "Can I replace a product that arrived damaged?"

    results = retrieve(query, k=3)

    print("\nQuery:")
    print(query)

    print("\nRetrieved chunks:\n")

    for result in results:
        print("=" * 70)
        print(f"Source: {result.source}")
        print(f"Chunk ID: {result.chunk_id}")
        print(f"Similarity: {result.similarity:.4f}")
        print(result.content)


if __name__ == "__main__":
    main()