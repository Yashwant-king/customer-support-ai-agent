from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.load_documents import load_documents


def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    chunks = []

    for document in documents:
        split_texts = splitter.split_text(document["content"])

        for index, text in enumerate(split_texts):
            chunks.append({
                "content": text,
                "source": document["source"],
                "chunk_id": index,
            })

    return chunks


def main():
    documents = load_documents()
    chunks = create_chunks(documents)

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    print("\nFirst 5 chunks:\n")

    for chunk in chunks[:5]:
        print("=" * 60)
        print(f"Source: {chunk['source']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(chunk["content"])


if __name__ == "__main__":
    main()