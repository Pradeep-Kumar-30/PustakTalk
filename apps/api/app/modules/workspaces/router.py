from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db_session
from app.modules.auth.dependencies import CurrentUser
from app.modules.workspaces.schemas import WorkspaceCreate, WorkspaceResponse
from app.modules.workspaces.service import WorkspaceService

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.get("", response_model=list[WorkspaceResponse])
def list_workspaces(
    user: CurrentUser, session: Annotated[Session, Depends(get_db_session)]
) -> list[WorkspaceResponse]:
    return [
        WorkspaceResponse.model_validate(item) for item in WorkspaceService(session).list(user.id)
    ]


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
def create_workspace(
    payload: WorkspaceCreate,
    user: CurrentUser,
    session: Annotated[Session, Depends(get_db_session)],
) -> WorkspaceResponse:
    return WorkspaceResponse.model_validate(WorkspaceService(session).create(user.id, payload))
