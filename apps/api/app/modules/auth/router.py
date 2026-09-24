from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.security import create_access_token
from app.infrastructure.database.session import get_db_session
from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.schemas import LoginRequest, RegisterRequest, UserResponse
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def set_session_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        secure=settings.auth_cookie_secure,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
        path="/",
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterRequest,
    response: Response,
    session: Annotated[Session, Depends(get_db_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> UserResponse:
    user = AuthService(session).register(payload)
    set_session_cookie(response, create_access_token(user.id, settings), settings)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=UserResponse)
def login(
    payload: LoginRequest,
    response: Response,
    session: Annotated[Session, Depends(get_db_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> UserResponse:
    user = AuthService(session).authenticate(payload)
    set_session_cookie(response, create_access_token(user.id, settings), settings)
    return UserResponse.model_validate(user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response) -> Response:
    response.delete_cookie("access_token", path="/")
    return response


@router.get("/me", response_model=UserResponse)
def current_user(user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(user)
