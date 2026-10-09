import os

from rag.retriever import retrieve

from llm import llm


SYSTEM_PROMPT = """
You are a customer support assistant. Answer using ONLY the provided policy context. 

Rules:
1. Do not invent policies or order details.
2. If info is missing, state you don't have enough information.
3. Do not make unsupported promises.
4. Provide a concise, helpful answer.
"""


def answer_question(question: str):

    results = retrieve(question, k=3)

    context_parts = []

    for result in results:
        context_parts.append(
            f"Source: {result.source}\n"
            f"{result.content}"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
{SYSTEM_PROMPT}

Company policy context:

{context}

Customer question:

{question}
"""

    response = llm.invoke(prompt)

    return response.content


def main():

    question = "Can I replace a product that arrived damaged?"

    answer = answer_question(question)

    print("\nCustomer:")
    print(question)

    print("\nAssistant:")
    print(answer)


if __name__ == "__main__":
    main()