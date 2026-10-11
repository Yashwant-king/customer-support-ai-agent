from langchain_core.tools import tool

from rag.retriever import retrieve



def search_company_policy(question: str) -> dict:
    """
    Search the company knowledge base for policies and support rules.

    Use this when answering questions about company policies,
    returns, refunds, cancellations, delivery, payments,
    warranties, verification, or escalation.
    """

    results = retrieve(question, k=3)

    if not results:
        return {
            "found": False,
            "message": "No relevant company policy was found."
        }

    policies = []

    for result in results:
        policies.append({
            "content": result.content,
            "source": result.source,
            "chunk_id": result.chunk_id,
            "similarity": float(result.similarity),
        })

    return {
        "found": True,
        "results": policies,
    }