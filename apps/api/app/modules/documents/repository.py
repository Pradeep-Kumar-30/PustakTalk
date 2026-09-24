from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.documents.models import Document, DocumentChunk, ProcessingJob


class DocumentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, document: Document) -> Document:
        self._session.add(document)
        self._session.flush()
        return document

    def get_owned(self, document_id: UUID, owner_id: UUID) -> Document | None:
        return self._session.scalar(
            select(Document)
            .join(Document.workspace)
            .where(Document.id == document_id, Document.workspace.has(owner_id=owner_id))
        )

    def list_workspace(self, workspace_id: UUID) -> list[Document]:
        return list(
            self._session.scalars(
                select(Document)
                .where(Document.workspace_id == workspace_id)
                .order_by(Document.created_at.desc())
            )
        )

    def add_job(self, document_id: UUID) -> ProcessingJob:
        job = ProcessingJob(document_id=document_id)
        self._session.add(job)
        self._session.flush()
        return job

    def latest_job(self, document_id: UUID) -> ProcessingJob | None:
        return self._session.scalar(
            select(ProcessingJob)
            .where(ProcessingJob.document_id == document_id)
            .order_by(ProcessingJob.created_at.desc())
        )

    def search_lexical(self, workspace_id: UUID, query: str, limit: int) -> list[DocumentChunk]:
        terms = [term for term in query.split() if len(term) > 1]
        statement = (
            select(DocumentChunk).join(Document).where(Document.workspace_id == workspace_id)
        )
        for term in terms[:8]:
            statement = statement.where(DocumentChunk.text.ilike(f"%{term}%"))
        return list(self._session.scalars(statement.limit(limit)))
