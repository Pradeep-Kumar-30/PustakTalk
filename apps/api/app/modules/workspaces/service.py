from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.modules.workspaces.models import Workspace
from app.modules.workspaces.repository import WorkspaceRepository
from app.modules.workspaces.schemas import WorkspaceCreate


class WorkspaceService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._workspaces = WorkspaceRepository(session)

    def create(self, owner_id: UUID, payload: WorkspaceCreate) -> Workspace:
        workspace = self._workspaces.add(
            Workspace(name=payload.name.strip(), description=payload.description, owner_id=owner_id)
        )
        self._session.commit()
        self._session.refresh(workspace)
        return workspace

    def list(self, owner_id: UUID) -> list[Workspace]:
        return self._workspaces.list_for_owner(owner_id)

    def require_owned(self, workspace_id: UUID, owner_id: UUID) -> Workspace:
        workspace = self._workspaces.get_owned(workspace_id, owner_id)
        if not workspace:
            raise NotFoundError("Workspace not found")
        return workspace
