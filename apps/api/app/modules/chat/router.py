from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.infrastructure.database.session import get_db_session
from app.modules.auth.dependencies import CurrentUser
from app.modules.chat.schemas import ChatRequest, ChatResponse, CitationResponse
from app.modules.chat.service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    user: CurrentUser,
    session: Annotated[Session, Depends(get_db_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> ChatResponse:
    result = ChatService(session, settings).respond(user.id, payload)
    return ChatResponse(
        conversation_id=result.conversation.id,
        message_id=result.message.id,
        intent=result.intent.value,
        answer=result.answer,
        citations=[CitationResponse.model_validate(item) for item in result.citations],
        grounded=result.grounded,
        created_at=result.message.created_at,
    )
