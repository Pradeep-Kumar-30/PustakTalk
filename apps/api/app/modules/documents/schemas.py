from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    original_filename: str
    status: str
    page_count: int | None
    failure_reason: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class DocumentDownloadResponse(BaseModel):
    url: str
    expires_in_seconds: int


class ProcessingStatusResponse(BaseModel):
    document_id: UUID
    status: str
    stage: str | None
    failure_reason: str | None
