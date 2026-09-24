from typing import TypedDict

from app.shared.enums import Intent


class AgentState(TypedDict):
    question: str
    intent: Intent
