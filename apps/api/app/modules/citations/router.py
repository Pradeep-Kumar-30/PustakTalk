from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.infrastructure.database.session import get_db_session
from app.modules.auth.dependencies import CurrentUser
from app.modules.chat.models import Citation, Message
from app.modules.chat.schemas import CitationResponse
from app.modules.conversations.models import Conversation

router = APIRouter(prefix="/citations", tags=["citations"])


@router.get("/{citation_id}", response_model=CitationResponse)
def get_citation(
    citation_id: UUID, user: CurrentUser, session: Annotated[Session, Depends(get_db_session)]
) -> CitationResponse:
    citation = session.scalar(
        select(Citation)
        .join(Message, Citation.message_id == Message.id)
        .join(Conversation, Message.conversation_id == Conversation.id)
        .where(Citation.id == citation_id, Conversation.user_id == user.id)
    )
    if not citation:
        raise NotFoundError("Citation not found")
    return CitationResponse.model_validate(citation)
