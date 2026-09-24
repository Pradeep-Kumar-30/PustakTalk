from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SelectedTextContext(BaseModel):
    document_id: UUID
    physical_page: int
    text: str = Field(min_length=1, max_length=12_000)
    surrounding_context: str | None = Field(default=None, max_length=12_000)


class ChatRequest(BaseModel):
    workspace_id: UUID
    question: str = Field(min_length=1, max_length=4000)
    conversation_id: UUID | None = None
    document_ids: list[UUID] | None = Field(default=None, max_length=20)
    selected_text: SelectedTextContext | None = None


class CitationResponse(BaseModel):
    id: UUID
    document_id: UUID
    document_name: str
    chunk_id: UUID
    physical_page: int
    logical_page: str | None
    source_text: str
    bbox: list[float] | None

    model_config = {"from_attributes": True}


class ChatResponse(BaseModel):
    conversation_id: UUID
    message_id: UUID
    intent: str
    answer: str
    citations: list[CitationResponse]
    grounded: bool
    created_at: datetime
