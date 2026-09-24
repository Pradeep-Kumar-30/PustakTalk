from sqlalchemy.orm import Session

from app.core.exceptions import AuthorizationError, ConflictError
from app.core.security import hash_password, verify_password
from app.modules.auth.models import User
from app.modules.auth.repository import UserRepository
from app.modules.auth.schemas import LoginRequest, RegisterRequest


class AuthService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._users = UserRepository(session)

    def register(self, payload: RegisterRequest) -> User:
        if self._users.get_by_email(payload.email):
            raise ConflictError("An account already exists for this email address")
        user = self._users.add(
            User(
                email=payload.email,
                password_hash=hash_password(payload.password),
                display_name=payload.display_name.strip(),
            )
        )
        self._session.commit()
        self._session.refresh(user)
        return user

    def authenticate(self, payload: LoginRequest) -> User:
        user = self._users.get_by_email(payload.email.strip().lower())
        if (
            not user
            or not user.is_active
            or not verify_password(payload.password, user.password_hash)
        ):
            raise AuthorizationError("Invalid email or password")
        return user
