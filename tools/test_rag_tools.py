from tools.rag_tools import search_company_policy


if __name__ == "__main__":
    question = input("Ask a policy question: ").strip()

    result = search_company_policy.invoke({
        "question": question
    })

    print("\nTool result:")
    print(result)