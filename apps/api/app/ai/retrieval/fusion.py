from uuid import UUID


def reciprocal_rank_fusion(
    rankings: list[dict[UUID, float]], constant: int = 60
) -> list[tuple[UUID, float]]:
    scores: dict[UUID, float] = {}
    for ranking in rankings:
        for rank, identifier in enumerate(sorted(ranking, key=ranking.get, reverse=True), start=1):
            scores[identifier] = scores.get(identifier, 0) + 1.0 / (constant + rank)
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)
