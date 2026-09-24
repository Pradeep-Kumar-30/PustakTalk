import re

from app.shared.types import ChunkEvidence


def has_sufficient_grounding(answer: str, evidence: list[ChunkEvidence]) -> bool:
    if not evidence:
        return "couldn't find sufficient evidence" in answer.lower()
    evidence_terms = set(re.findall(r"\w{5,}", " ".join(item.text.lower() for item in evidence)))
    answer_terms = set(re.findall(r"\w{5,}", answer.lower()))
    return not answer_terms or len(answer_terms & evidence_terms) / len(answer_terms) >= 0.08
