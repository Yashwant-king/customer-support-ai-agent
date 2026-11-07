
import json


def calculate_metrics():

    # Load evaluation results
    with open(
        "evaluation/new_evaluation_results.json",
        "r",
        encoding="utf-8"
    ) as file:

        results = json.load(file)

    total_cases = len(results)

    # Tool selection
    tool_correct = sum(
        r["tool_selection"]["passed"]
        for r in results
    )

    tool_accuracy = (
        tool_correct / total_cases * 100
        if total_cases else 0
    )

    # Risk classification
    risk_correct = sum(
        r["risk_classification"]["passed"]
        for r in results
    )

    risk_accuracy = (
        risk_correct / total_cases * 100
        if total_cases else 0
    )

    # Execution success
    successful = sum(
        r.get("actual_output", {}).get("status") == "success"
        for r in results
    )

    success_rate = (
        successful / total_cases * 100
        if total_cases else 0
    )

    # Average latency of successful executions
    latencies = [
        r["actual_output"]["execution_time"]
        for r in results
        if r.get("actual_output", {}).get("status") == "success"
    ]

    average_latency = (
        sum(latencies) / len(latencies)
        if latencies else 0
    )

    return {
        "total_cases": total_cases,
        "tool_selection_accuracy": round(tool_accuracy, 2),
        "risk_classification_accuracy": round(risk_accuracy, 2),
        "execution_success_rate": round(success_rate, 2),
        "average_latency_seconds": round(average_latency, 3)
    }


if __name__ == "__main__":

    metrics = calculate_metrics()

    print("\n========== EVALUATION METRICS ==========\n")
    with open("evaluation/metrics_result.json","w", encoding="utf-8") as metrics_file:
        json.dump(metrics, metrics_file, indent=4, ensure_ascii=False)

    print(json.dumps(
        metrics,
        indent=4
    ))


