from app.ai.llm.base import LLMProvider
from app.ai.prompts.rag import make_rag_prompt
from app.ai.prompts.system import SYSTEM_PROMPT
from app.shared.types import ChunkEvidence


class AnswerGenerator:
    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm

    def generate(
        self, question: str, memory: str, context: str, evidence: list[ChunkEvidence]
    ) -> str:
        if not evidence:
            return "I couldn't find sufficient evidence for this in the uploaded documents."
        try:
            answer = self._llm.generate(SYSTEM_PROMPT, make_rag_prompt(question, memory, context))
        except Exception:
            return (
                "I found this relevant passage, but the local language model is unavailable: "
                f"{evidence[0].text[:700]}"
            )
        return answer or "I couldn't produce a grounded answer from the retrieved evidence."
