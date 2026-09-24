from typing import Any
from uuid import UUID

from sqlalchemy import JSON, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, UUIDTimestampMixin


class Message(UUIDTimestampMixin, Base):
    __tablename__ = "messages"

    conversation_id: Mapped[UUID] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    intent: Mapped[str | None] = mapped_column(String(40), nullable=True)
    metadata_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class Citation(UUIDTimestampMixin, Base):
    __tablename__ = "citations"

    message_id: Mapped[UUID] = mapped_column(
        ForeignKey("messages.id", ondelete="CASCADE"), index=True
    )
    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True
    )
    chunk_id: Mapped[UUID] = mapped_column(
        ForeignKey("document_chunks.id", ondelete="CASCADE"), index=True
    )
    document_name: Mapped[str] = mapped_column(String(255))
    physical_page: Mapped[int] = mapped_column(Integer)
    logical_page: Mapped[str | None] = mapped_column(String(32), nullable=True)
    source_text: Mapped[str] = mapped_column(Text)
    bbox: Mapped[list[float] | None] = mapped_column(JSON, nullable=True)
