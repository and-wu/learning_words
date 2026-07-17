from fastapi import Cookie, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.services.current_user_service import CurrentUserService


# Создает сервис получения текущего пользователя
def get_current_user_service(db: Session = Depends(get_db)) -> CurrentUserService:

    return CurrentUserService(
        user_repository=UserRepository(db),
        session_repository=SessionRepository(db),
    )


# Возвращает авторизованного пользователя по session_token
def get_current_user(
    session_token: str | None = Cookie(default=None),
    service: CurrentUserService = Depends(get_current_user_service),
) -> User:

    return service.get_current_user(session_token)