from app.ai.agents.router import classify_intent
from app.shared.enums import Intent


def test_hinglish_page_query_uses_deterministic_page_search() -> None:
    assert classify_intent("Congestion control kis page par hai?") == Intent.PAGE_SEARCH


def test_exam_question_query_uses_study_material() -> None:
    assert classify_intent("Is topic se 5 exam questions banao") == Intent.STUDY_MATERIAL
