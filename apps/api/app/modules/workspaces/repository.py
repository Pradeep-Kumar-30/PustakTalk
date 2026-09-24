from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.workspaces.models import Workspace


class WorkspaceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_for_owner(self, owner_id: UUID) -> list[Workspace]:
        return list(
            self._session.scalars(
                select(Workspace)
                .where(Workspace.owner_id == owner_id)
                .order_by(Workspace.created_at.desc())
            )
        )

    def get_owned(self, workspace_id: UUID, owner_id: UUID) -> Workspace | None:
        return self._session.scalar(
            select(Workspace).where(Workspace.id == workspace_id, Workspace.owner_id == owner_id)
        )

    def add(self, workspace: Workspace) -> Workspace:
        self._session.add(workspace)
        self._session.flush()
        return workspace
