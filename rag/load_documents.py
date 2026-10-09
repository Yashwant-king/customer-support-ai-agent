from pathlib import Path


KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"


def load_documents():
    documents = []

    for file_path in KNOWLEDGE_DIR.rglob("*.md"):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "source": str(file_path.relative_to(KNOWLEDGE_DIR)),
            "content": text,
        })

    return documents


def main():
    documents = load_documents()

    # print(f"Documents loaded: {len(documents)}")
    # print(type(documents[0]))
    # for document in documents:
    #     print(f"\n--- {document['source']} ---")
    #     print(f"Characters: {len(document['content'])}")

     

if __name__ == "__main__":
    main()