from typing import Annotated

from fastapi import Cookie, Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.exceptions import AuthorizationError
from app.core.security import read_access_token
from app.infrastructure.database.session import get_db_session
from app.modules.auth.models import User
from app.modules.auth.repository import UserRepository


def get_current_user(
    session: Annotated[Session, Depends(get_db_session)],
    settings: Annotated[Settings, Depends(get_settings)],
    access_token: Annotated[str | None, Cookie()] = None,
) -> User:
    if not access_token:
        raise AuthorizationError("Sign in is required")
    user_id = read_access_token(access_token, settings)
    user = UserRepository(session).get(user_id)
    if not user or not user.is_active:
        raise AuthorizationError("Sign in is required")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
