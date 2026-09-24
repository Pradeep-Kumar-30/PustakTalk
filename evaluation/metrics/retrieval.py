from collections.abc import Iterable


def recall_at_k(retrieved: Iterable[str], relevant: set[str], k: int) -> float:
    if not relevant:
        return 1.0
    return len(set(list(retrieved)[:k]) & relevant) / len(relevant)


def precision_at_k(retrieved: Iterable[str], relevant: set[str], k: int) -> float:
    values = list(retrieved)[:k]
    return len(set(values) & relevant) / k if k else 0.0
