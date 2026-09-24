from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.infrastructure.database.session import get_db_session
from app.infrastructure.queue.publisher import enqueue_document_processing
from app.infrastructure.storage.minio import MinioObjectStorage
from app.modules.auth.dependencies import CurrentUser
from app.modules.documents.schemas import (
    DocumentDownloadResponse,
    DocumentResponse,
    ProcessingStatusResponse,
)
from app.modules.documents.service import DocumentService

router = APIRouter(tags=["documents"])


def get_document_service(
    session: Annotated[Session, Depends(get_db_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> DocumentService:
    return DocumentService(session, MinioObjectStorage.from_settings(settings), settings)


@router.post(
    "/workspaces/{workspace_id}/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_document(
    workspace_id: UUID,
    file: Annotated[UploadFile, File()],
    user: CurrentUser,
    service: Annotated[DocumentService, Depends(get_document_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> DocumentResponse:
    content = await file.read(settings.max_upload_bytes + 1)
    try:
        document = service.upload(
            workspace_id, user.id, file.filename or "document.pdf", file.content_type or "", content
        )
        await enqueue_document_processing(document.id, settings)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return DocumentResponse.model_validate(document)


@router.get("/workspaces/{workspace_id}/documents", response_model=list[DocumentResponse])
def list_documents(
    workspace_id: UUID,
    user: CurrentUser,
    service: Annotated[DocumentService, Depends(get_document_service)],
) -> list[DocumentResponse]:
    return [
        DocumentResponse.model_validate(item)
        for item in service.list_workspace(workspace_id, user.id)
    ]


@router.get("/documents/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: UUID,
    user: CurrentUser,
    service: Annotated[DocumentService, Depends(get_document_service)],
) -> DocumentResponse:
    return DocumentResponse.model_validate(service.require_owned(document_id, user.id))


@router.get("/documents/{document_id}/status", response_model=ProcessingStatusResponse)
def get_processing_status(
    document_id: UUID,
    user: CurrentUser,
    service: Annotated[DocumentService, Depends(get_document_service)],
) -> ProcessingStatusResponse:
    document, job = service.status(document_id, user.id)
    return ProcessingStatusResponse(
        document_id=document.id,
        status=document.status,
        stage=job.stage if job else None,
        failure_reason=document.failure_reason,
    )


@router.post(
    "/documents/{document_id}/retry",
    response_model=DocumentResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def retry_document(
    document_id: UUID,
    user: CurrentUser,
    service: Annotated[DocumentService, Depends(get_document_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> DocumentResponse:
    document = service.retry(document_id, user.id)
    await enqueue_document_processing(document.id, settings)
    return DocumentResponse.model_validate(document)


@router.get("/documents/{document_id}/download", response_model=DocumentDownloadResponse)
def get_document_download_url(
    document_id: UUID,
    user: CurrentUser,
    service: Annotated[DocumentService, Depends(get_document_service)],
) -> DocumentDownloadResponse:
    return DocumentDownloadResponse(
        url=service.get_download_url(document_id, user.id), expires_in_seconds=900
    )


@router.get("/documents/{document_id}/content")
def get_document_content(
    document_id: UUID,
    user: CurrentUser,
    service: Annotated[DocumentService, Depends(get_document_service)],
) -> Response:
    content, filename = service.download_content(document_id, user.id)
    return Response(
        content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="{filename}"',
            "Cache-Control": "private, no-store",
        },
    )
