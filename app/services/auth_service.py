from datetime import datetime, UTC, timedelta

from fastapi import HTTPException, status

from app.models.session import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.session_repository import SessionRepository
from app.schemas.auth import RegisterRequest, LoginRequest
from app.services.password_service import PasswordService
from app.services.token_service import TokenService

SESSION_LIFETIME_DAYS = 30

class AuthService:
    def __init__(
            self,
            user_repository: UserRepository,
            session_repository: SessionRepository,
    ):
        self.user_repository = user_repository
        self.session_repository = session_repository

    # Авторизация пользователя
    def login(self, data: LoginRequest) -> Session:

        user = self._authenticate_user(data)

        return self._create_session(user.id)

    # Регистрация пользователя
    def register(self, data: RegisterRequest) -> User:

        self._validate_registration(data)

        return self._create_user(data)

    # Выход пользователя
    def logout(self, session_token: str,) -> None:

        session = self._get_session(session_token)

        self.session_repository.delete(session)

    # Проверяет логин и пароль пользователя
    def _authenticate_user(self, data: LoginRequest) -> User:

        user = self.user_repository.get_by_login(data.login)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid login or password",
            )

        if not PasswordService.verify_password(
            data.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid login or password",
            )

        return user

    # Создает новую пользовательскую сессию
    # ==========================================
    def _create_session(self, user_id: int) -> Session:

        session = Session(
            user_id=user_id,
            session_token=TokenService.generate_session_token(),
            expires_at=datetime.now(UTC)
            + timedelta(days=SESSION_LIFETIME_DAYS),
        )

        return self.session_repository.create(session)

    # Проверяет возможность регистрации
    def _validate_registration(self, data: RegisterRequest) -> None:

        email = str(data.email).lower()

        if self.user_repository.get_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )

        if self.user_repository.get_by_login(data.login):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Login already exists",
            )

    # Создает нового пользователя
    def _create_user(self, data: RegisterRequest) -> User:

        password_hash = PasswordService.hash_password(
            data.password,
        )

        user = User(
            email=str(data.email).lower(),
            login=data.login,
            name=data.name,
            password_hash=password_hash,
            role=data.role,
        )

        return self.user_repository.create(user)

    # Возвращает сессию по токену
    def _get_session(self, session_token: str) -> Session:

        session = self.session_repository.get_by_token(session_token)

        if session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        return session