import re

from app.shared.enums import Intent


def classify_intent(question: str) -> Intent:
    normalized = question.lower()
    if re.search(
        r"\b(kis|kaun|which|what)\s+page\b|\bpage\s*(par|number|no|\?)|किस पेज", normalized
    ):
        return Intent.PAGE_SEARCH
    if any(term in normalized for term in ("exact word", "find exact", "search word", "शब्द खोज")):
        return Intent.EXACT_SEARCH
    if any(term in normalized for term in ("compare", "तुलना", "difference between")):
        return Intent.MULTI_DOCUMENT_COMPARE
    if any(
        term in normalized
        for term in ("mcq", "exam question", "questions banao", "flashcard", "revision notes")
    ):
        return Intent.STUDY_MATERIAL
    if any(
        term in normalized
        for term in ("summarize page", "page summary", "chapter summary", "summary")
    ):
        return Intent.PAGE_SUMMARY
    return Intent.DOCUMENT_QA
