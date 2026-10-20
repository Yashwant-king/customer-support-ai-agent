
import json
from pathlib import Path
from typing import Any, cast

from graph.main import app
from database import customer_service
from graph.random_id import get_random_customer_id


DATASET_PATH = Path(__file__).parent / "eval_dataset.jsonl"


def load_dataset():
    cases = []

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                case = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON on line {line_number}"
                ) from error

            if "id" not in case or "query" not in case:
                raise ValueError(
                    f"Line {line_number} needs id and query."
                )

            if (
                "expected_functions" not in case
                and case.get("expected_risk") != "unsafe"
            ):
                raise ValueError(
                    f"Line {line_number} needs expected_functions."
                )

            cases.append(case)

    return cases


def calculate_metrics(expected, actual):
    expected = set(expected)
    actual = set(actual)
    overlap = len(expected & actual)

    precision = (
        overlap / len(actual)
        if actual
        else (1.0 if not expected else 0.0)
    )

    recall = (
        overlap / len(expected)
        if expected
        else (1.0 if not actual else 0.0)
    )

    return {
        "precision": precision,
        "recall": recall,
        "exact_match": expected == actual,
    }


def main():
    cases = load_dataset()

    if not cases:
        raise ValueError("Evaluation dataset is empty.")

    # Use a valid customer from your development database.
    customer_id = str(get_random_customer_id())

    if not customer_id:
        raise ValueError(
            "No test customer was found in the database."
        )

    results = []

    for case in cases:
        print(f"\nRunning {case['id']}: {case['query']}")

        state = {
            "messages": [],
            "customer_id": customer_id,
            "customer_query": case["query"],
        }

        try:
            output = app.invoke(
                cast(Any, state),
                config={
                    "configurable": {
                        "thread_id": f"evaluation-{case['id']}"
                    }
                },
            )

            actual_functions = list(dict.fromkeys(
                output.get("node_1", [])
                + output.get("node_2", [])
            ))

            expected_functions = case.get(
                "expected_functions", []
            )

            metrics = calculate_metrics(
                expected_functions,
                actual_functions,
            )

            # This is an initial routing-based risk check.
            # It assumes unsafe queries terminate before node_1.
            actual_risk = (
                "safe" if "node_1" in output else "unsafe"
            )

            risk_correct = (
                actual_risk == case["expected_risk"]
                if "expected_risk" in case
                else None
            )

            result = {
                "id": case["id"],
                "expected_functions": expected_functions,
                "actual_functions": actual_functions,
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "exact_match": metrics["exact_match"],
                "expected_risk": case.get("expected_risk"),
                "actual_risk": actual_risk,
                "risk_correct": risk_correct,
                "final_result": output.get("final_result"),
                "error": None,
            }

        except Exception as error:
            result = {
                "id": case["id"],
                "error": str(error),
            }

        results.append(result)

        if result["error"]:
            print(f"ERROR: {result['error']}")
        else:
            print("Expected:", result["expected_functions"])
            print("Actual:  ", result["actual_functions"])
            print("Exact match:", result["exact_match"])
            if result["risk_correct"] is not None:
                print("Risk correct:", result["risk_correct"])

    successful = [r for r in results if not r.get("error")]

    if successful:
        exact_accuracy = sum(
            r["exact_match"] for r in successful
        ) / len(successful)

        print("\n========== EVALUATION SUMMARY ==========")
        print(f"Total cases: {len(cases)}")
        print(f"Successful runs: {len(successful)}")
        print(f"Failed runs: {len(cases) - len(successful)}")
        print(f"Function exact-match accuracy: {exact_accuracy:.2%}")

        risk_results = [
            r for r in successful
            if r["risk_correct"] is not None
        ]

        if risk_results:
            risk_accuracy = sum(
                r["risk_correct"] for r in risk_results
            ) / len(risk_results)

            print(f"Routing-based risk accuracy: {risk_accuracy:.2%}")

    # Save detailed results for later analysis.
    output_path = Path(__file__).parent / "eval_results.json"
    output_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"\nDetailed results saved to: {output_path}")


if __name__ == "__main__":
    main()
