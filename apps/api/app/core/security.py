from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from pwdlib import PasswordHash

from app.core.config import Settings
from app.core.exceptions import AuthorizationError

_password_hash = PasswordHash.recommended()
_ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return _password_hash.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return _password_hash.verify(password, password_hash)


def create_access_token(user_id: UUID, settings: Settings) -> str:
    expires_at = datetime.now(UTC) + timedelta(days=7)
    return jwt.encode(
        {"sub": str(user_id), "exp": expires_at}, settings.auth_secret, algorithm=_ALGORITHM
    )


def read_access_token(token: str, settings: Settings) -> UUID:
    try:
        payload = jwt.decode(token, settings.auth_secret, algorithms=[_ALGORITHM])
        return UUID(payload["sub"])
    except (jwt.InvalidTokenError, ValueError, KeyError) as error:
        raise AuthorizationError("Your session has expired. Please sign in again.") from error
