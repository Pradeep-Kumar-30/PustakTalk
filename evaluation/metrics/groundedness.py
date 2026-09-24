import re


def lexical_groundedness(answer: str, sources: list[str]) -> float:
    terms = set(re.findall(r"\w{5,}", answer.lower()))
    if not terms:
        return 1.0
    evidence = set(re.findall(r"\w{5,}", " ".join(sources).lower()))
    return len(terms & evidence) / len(terms)
