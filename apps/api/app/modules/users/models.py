from uuid import UUID

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, UUIDTimestampMixin


class UserSettings(UUIDTimestampMixin, Base):
    __tablename__ = "user_settings"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True
    )
    preferences: Mapped[dict[str, str | bool | int]] = mapped_column(JSON, default=dict)
