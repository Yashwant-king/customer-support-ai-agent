def tool_selection_evaluator(
    expected_functions: list,
    actual_functions: list
):

    expected = set(expected_functions)
    actual = set(actual_functions)

    score = expected == actual

    return {
        "score": int(score),
        "passed": score,
        "expected": sorted(expected),
        "actual": sorted(actual)
    }






def risk_classification_evaluator(
    expected_risk: str,
    actual_risk: str
):

    score = (
        expected_risk.lower()
        == actual_risk.lower()
    )

    return {
        "score": int(score),
        "passed": score,
        "expected": expected_risk,
        "actual": actual_risk
    }



