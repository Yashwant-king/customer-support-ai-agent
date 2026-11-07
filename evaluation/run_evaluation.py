import json

from dotenv import load_dotenv

load_dotenv()

from evaluation.target import target

from evaluation.evaluators import (
    tool_selection_evaluator,
    risk_classification_evaluator
)



def run_evaluation():

    results = []

    dataset_path = "evaluation/eval_dataset.jsonl"

    # 1. Read evaluation dataset
    with open(
        dataset_path,
        "r",
        encoding="utf-8"
    ) as file:

        for line_number, line in enumerate(file, start=1):
            print(f"\nProcessing line {line_number}...")

            # Skip blank lines
            if not line.strip():
                continue

            # 2. Parse JSON safely
            try:
                test_case = json.loads(line)

            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Invalid JSON at line {line_number}: {e}"
                ) from e

            print(f"\nEvaluating: {test_case['id']}")
            print(f"Query: {test_case['query']}")

            # 3. Execute LangGraph agent
            print(f"Executing target function for test case {test_case['id']}...")
            actual = target({
                "query": test_case["query"],
                "type": test_case["type"]
            })

            # 4. Evaluate tool selection
            print(f"Evaluating tool selection for test case {test_case['id']}...")
            tool_result = tool_selection_evaluator(
                test_case.get("expected_functions", []),
                actual.get("node_1", [])
            )

            # 5. Evaluate risk classification
            print(f"Evaluating risk classification for test case {test_case['id']}...")
            risk_result = risk_classification_evaluator(
                test_case["expected_risk"],
                actual.get("risk", "")
            )

            # 6. Store results
            results.append({
                "id": test_case["id"],
                "type": test_case["type"],
                "query": test_case["query"],
                "tool_selection": tool_result,
                "risk_classification": risk_result
            })

            print("Tool Selection:", tool_result["passed"])
            print("Risk Classification:", risk_result["passed"])

    return results


if __name__ == "__main__":

    print("\nStarting LangGraph Evaluation...\n")

    evaluation_results = run_evaluation()

    # 7. Display complete results
    print("\n========== EVALUATION RESULTS ==========\n")

    print(json.dumps(
        evaluation_results,
        indent=4,
        ensure_ascii=False
    ))

    # 8. Save results
    with open(
        "evaluation/new_evaluation_results.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            evaluation_results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nEvaluation completed!")
    print("Results saved to evaluation/evaluation_results.json")


