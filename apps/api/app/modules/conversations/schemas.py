from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ConversationMessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    intent: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
