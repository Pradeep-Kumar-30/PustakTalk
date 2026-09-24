from app.modules.chat.models import Message


def compact_memory(summary: str | None, recent_messages: list[Message]) -> str:
    recent = "\n".join(f"{message.role}: {message.content[:500]}" for message in recent_messages)
    return "\n".join(part for part in (summary, recent) if part)[:5000]
