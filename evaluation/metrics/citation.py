def citation_accuracy(
    citations: list[dict[str, object]], valid_chunk_ids: set[str]
) -> float:
    if not citations:
        return 0.0
    valid = sum(
        str(citation.get("chunk_id")) in valid_chunk_ids for citation in citations
    )
    return valid / len(citations)
