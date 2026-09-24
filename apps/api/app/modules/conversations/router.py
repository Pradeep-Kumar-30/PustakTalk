from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db_session
from app.modules.auth.dependencies import CurrentUser
from app.modules.conversations.schemas import ConversationMessageResponse
from app.modules.conversations.service import ConversationService

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get("/{conversation_id}/messages", response_model=list[ConversationMessageResponse])
def get_messages(
    conversation_id: UUID,
    workspace_id: Annotated[UUID, Query()],
    user: CurrentUser,
    session: Annotated[Session, Depends(get_db_session)],
) -> list[ConversationMessageResponse]:
    messages = ConversationService(session).messages(conversation_id, workspace_id, user.id)
    return [ConversationMessageResponse.model_validate(message) for message in messages]
