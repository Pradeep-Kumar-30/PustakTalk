from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import JSON, BigInteger, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base, UUIDTimestampMixin
from app.shared.enums import DocumentStatus

if TYPE_CHECKING:
    from app.modules.workspaces.models import Workspace


class Document(UUIDTimestampMixin, Base):
    __tablename__ = "documents"

    workspace_id: Mapped[UUID] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"), index=True
    )
    original_filename: Mapped[str] = mapped_column(String(255))
    storage_key: Mapped[str] = mapped_column(String(512), unique=True)
    content_type: Mapped[str] = mapped_column(String(100))
    size_bytes: Mapped[int] = mapped_column(BigInteger)
    status: Mapped[str] = mapped_column(
        String(20), default=DocumentStatus.UPLOADED.value, index=True
    )
    page_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    workspace: Mapped["Workspace"] = relationship(back_populates="documents")
    pages: Mapped[list["DocumentPage"]] = relationship(cascade="all, delete-orphan")
    chunks: Mapped[list["DocumentChunk"]] = relationship(cascade="all, delete-orphan")


class DocumentPage(UUIDTimestampMixin, Base):
    __tablename__ = "document_pages"
    __table_args__ = (
        UniqueConstraint("document_id", "physical_page", name="document_page_number"),
    )

    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True
    )
    physical_page: Mapped[int] = mapped_column(Integer)
    logical_page: Mapped[str | None] = mapped_column(String(32), nullable=True)
    extracted_text: Mapped[str] = mapped_column(Text)
    extraction_method: Mapped[str] = mapped_column(String(20))
    text_quality_score: Mapped[float] = mapped_column()
    dimensions: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class DocumentChunk(UUIDTimestampMixin, Base):
    __tablename__ = "document_chunks"
    __table_args__ = (UniqueConstraint("document_id", "chunk_key", name="document_chunk_key"),)

    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True
    )
    physical_page: Mapped[int] = mapped_column(Integer, index=True)
    logical_page: Mapped[str | None] = mapped_column(String(32), nullable=True)
    chunk_key: Mapped[str] = mapped_column(String(100))
    text: Mapped[str] = mapped_column(Text)
    heading: Mapped[str | None] = mapped_column(String(500), nullable=True)
    section: Mapped[str | None] = mapped_column(String(500), nullable=True)
    bbox: Mapped[list[float] | None] = mapped_column(JSON, nullable=True)
    token_count: Mapped[int] = mapped_column(Integer)
    extraction_method: Mapped[str] = mapped_column(String(20))


class ProcessingJob(UUIDTimestampMixin, Base):
    __tablename__ = "processing_jobs"

    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[str] = mapped_column(String(20), default="queued", index=True)
    stage: Mapped[str] = mapped_column(String(40), default="queued")
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
