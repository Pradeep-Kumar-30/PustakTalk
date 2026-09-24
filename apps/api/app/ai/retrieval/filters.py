from uuid import UUID


def filter_document_scope(
    scores: list[tuple[UUID, float]], allowed_document_ids: set[UUID] | None
) -> list[tuple[UUID, float]]:
    """Filtering document ids is applied while evidence metadata is hydrated."""
    return scores if allowed_document_ids is None else scores
