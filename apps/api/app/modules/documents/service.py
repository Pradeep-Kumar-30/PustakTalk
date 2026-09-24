import re
from pathlib import PurePath
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.exceptions import NotFoundError
from app.infrastructure.storage.base import ObjectStorage
from app.modules.documents.models import Document, ProcessingJob
from app.modules.documents.repository import DocumentRepository
from app.modules.workspaces.service import WorkspaceService
from app.shared.enums import DocumentStatus


class DocumentService:
    def __init__(self, session: Session, storage: ObjectStorage, settings: Settings) -> None:
        self._session = session
        self._storage = storage
        self._settings = settings
        self._documents = DocumentRepository(session)
        self._workspaces = WorkspaceService(session)

    def upload(
        self, workspace_id: UUID, owner_id: UUID, filename: str, content_type: str, content: bytes
    ) -> Document:
        self._workspaces.require_owned(workspace_id, owner_id)
        self._validate_pdf(filename, content_type, content)
        safe_name = self._safe_filename(filename)
        document = Document(
            workspace_id=workspace_id,
            original_filename=safe_name,
            storage_key=f"workspaces/{workspace_id}/documents/{uuid4()}.pdf",
            content_type="application/pdf",
            size_bytes=len(content),
        )
        self._storage.upload(document.storage_key, content, "application/pdf")
        self._documents.add(document)
        self._documents.add_job(document.id)
        self._session.commit()
        self._session.refresh(document)
        return document

    def list_workspace(self, workspace_id: UUID, owner_id: UUID) -> list[Document]:
        self._workspaces.require_owned(workspace_id, owner_id)
        return self._documents.list_workspace(workspace_id)

    def require_owned(self, document_id: UUID, owner_id: UUID) -> Document:
        document = self._documents.get_owned(document_id, owner_id)
        if not document:
            raise NotFoundError("Document not found")
        return document

    def status(self, document_id: UUID, owner_id: UUID) -> tuple[Document, ProcessingJob | None]:
        return self.require_owned(document_id, owner_id), self._documents.latest_job(document_id)

    def get_download_url(self, document_id: UUID, owner_id: UUID) -> str:
        document = self.require_owned(document_id, owner_id)
        return self._storage.get_signed_url(document.storage_key)

    def retry(self, document_id: UUID, owner_id: UUID) -> Document:
        document = self.require_owned(document_id, owner_id)
        document.status = DocumentStatus.UPLOADED.value
        document.failure_reason = None
        self._documents.add_job(document.id)
        self._session.commit()
        self._session.refresh(document)
        return document

    def download_content(self, document_id: UUID, owner_id: UUID) -> tuple[bytes, str]:
        document = self.require_owned(document_id, owner_id)
        return self._storage.download(document.storage_key), document.original_filename

    def _validate_pdf(self, filename: str, content_type: str, content: bytes) -> None:
        if not filename.lower().endswith(".pdf") or content_type not in {"application/pdf", ""}:
            raise ValueError("Only PDF uploads are accepted")
        if not content.startswith(b"%PDF-"):
            raise ValueError("Uploaded file is not a valid PDF")
        if len(content) > self._settings.max_upload_bytes:
            raise ValueError(
                f"PDF exceeds the {self._settings.max_upload_bytes // 1_048_576} MB limit"
            )

    @staticmethod
    def _safe_filename(filename: str) -> str:
        basename = PurePath(filename).name
        cleaned = re.sub(r"[^\w. -]", "_", basename, flags=re.UNICODE).strip(". ")
        return (cleaned[:200] or "document") + ("" if cleaned.lower().endswith(".pdf") else ".pdf")
