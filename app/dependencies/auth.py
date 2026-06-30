from fastapi import Cookie, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.services.current_user_service import CurrentUserService

def get_current_user(
        session_token: str | None = Cookie(default=None),
        db: Session = Depends(get_db)
    )-> User:

    user_repository = UserRepository(db)
    session_repository = SessionRepository(db)

    service = CurrentUserService(
        user_repository=user_repository,
        session_repository=session_repository,
    )

    return service.get_current_user(session_token)