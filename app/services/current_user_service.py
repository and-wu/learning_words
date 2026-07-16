from datetime import datetime, UTC

from fastapi import HTTPException, status

from app.models.session import Session
from app.models.user import User
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository


class CurrentUserService:

    def __init__(
        self,
        user_repository: UserRepository,
        session_repository: SessionRepository,
    ):
        self.user_repository = user_repository
        self.session_repository = session_repository

    # ==========================================================
    # Public methods
    # ==========================================================

    # Возвращает текущего авторизованного пользователя по session_token
    def get_current_user(self, session_token: str | None) -> User:

        session = self._get_session(session_token)

        return self._get_user(session.user_id)

    # ==========================================================
    # Private methods
    # ==========================================================

    # Возвращает активную сессию пользователя
    def _get_session(self, session_token: str | None) -> Session:

        if session_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        session = self.session_repository.get_by_token(session_token)

        if session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        if session.expires_at < datetime.now(UTC):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired",
            )

        return session

    # Возвращает пользователя по id
    def _get_user(self, user_id: int) -> User:

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        return user