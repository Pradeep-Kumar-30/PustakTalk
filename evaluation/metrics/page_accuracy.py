def page_accuracy(predicted: list[int], expected: set[int]) -> float:
    return float(bool(set(predicted) & expected)) if expected else 1.0
