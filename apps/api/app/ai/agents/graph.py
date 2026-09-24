from functools import lru_cache

from langgraph.graph import END, START, StateGraph

from app.ai.agents.router import classify_intent
from app.ai.agents.state import AgentState
from app.shared.enums import Intent


def _classify(state: AgentState) -> AgentState:
    return {**state, "intent": classify_intent(state["question"])}


@lru_cache
def get_intent_graph():
    graph = StateGraph(AgentState)
    graph.add_node("classify_intent", _classify)
    graph.add_edge(START, "classify_intent")
    graph.add_edge("classify_intent", END)
    return graph.compile()


def resolve_intent(question: str) -> Intent:
    return get_intent_graph().invoke({"question": question, "intent": classify_intent(question)})[
        "intent"
    ]
