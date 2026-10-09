from pathlib import Path

from rag.retriever import retrieve


TEST_CASES = [
    {
        "question": "Can I replace a product that arrived damaged?",
        "expected_sources": [
            "returns/replacement_policy.md",
            "delivery/damaged_package.md",
        ],
    },
    {
        "question": "Can I cancel my order?",
        "expected_sources": [
            "orders/order_cancellation.md",
        ],
    },
    {
        "question": "My package has not arrived yet.",
        "expected_sources": [
            "delivery/delayed_delivery.md",
            "delivery/lost_package.md",
        ],
    },
    {
        "question": "I have not received my refund.",
        "expected_sources": [
            "payments/refund_processing.md",
            "returns/refund_policy.md",
        ],
    },
    {
        "question": "I want to speak to a human agent.",
        "expected_sources": [
            "support/human_handoff.md",
            "support/escalation_policy.md",
        ],
    },
]


def normalize_path(path):
    return Path(path).as_posix()


def main():
    total = len(TEST_CASES)
    passed = 0

    for i, test in enumerate(TEST_CASES, start=1):

        results = retrieve(test["question"], k=3)

        retrieved_sources = [
            normalize_path(result.source)
            for result in results
        ]

        expected_sources = [
            normalize_path(source)
            for source in test["expected_sources"]
        ]

        retrieved_set = set(retrieved_sources)

        matched = any(
            source in retrieved_set
            for source in expected_sources
        )

        if matched:
            passed += 1

        print("=" * 70)
        print(f"Test {i}")
        print(f"Question: {test['question']}")
        print(f"Retrieved: {retrieved_sources}")
        print(f"Expected: {expected_sources}")
        print(f"Result: {'PASS' if matched else 'FAIL'}")

    print("\n" + "=" * 70)
    print(f"Retrieval accuracy: {passed}/{total}")


if __name__ == "__main__":
    main()