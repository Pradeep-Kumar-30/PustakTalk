from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.chat.models import Message
from app.modules.conversations.models import Conversation


class ConversationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_owned(
        self, conversation_id: UUID, workspace_id: UUID, user_id: UUID
    ) -> Conversation | None:
        return self._session.scalar(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.workspace_id == workspace_id,
                Conversation.user_id == user_id,
            )
        )

    def add(self, conversation: Conversation) -> Conversation:
        self._session.add(conversation)
        self._session.flush()
        return conversation

    def recent_messages(self, conversation_id: UUID, limit: int = 8) -> list[Message]:
        messages = list(
            self._session.scalars(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .limit(limit)
            )
        )
        return list(reversed(messages))
