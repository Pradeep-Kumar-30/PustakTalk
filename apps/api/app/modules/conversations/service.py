from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.modules.conversations.repository import ConversationRepository


class ConversationService:
    def __init__(self, session: Session) -> None:
        self._repository = ConversationRepository(session)

    def messages(self, conversation_id: UUID, workspace_id: UUID, user_id: UUID):
        if not self._repository.get_owned(conversation_id, workspace_id, user_id):
            raise NotFoundError("Conversation not found")
        return self._repository.recent_messages(conversation_id, limit=100)
