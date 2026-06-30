from datetime import datetime, UTC, timedelta

from fastapi import HTTPException, status

from app.models.session import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.session_repository import SessionRepository
from app.schemas.auth import RegisterRequest, LoginRequest
from app.services.password_service import PasswordService
from app.services.token_service import TokenService


class AuthService:
    def __init__(
            self,
            user_repository: UserRepository,
            session_repository: SessionRepository,
    ):
        self.user_repository = user_repository
        self.session_repository = session_repository

    def login(self, data: LoginRequest) -> Session:

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

        token = TokenService.generate_session_token()

        session = Session(
            user_id=user.id,
            session_token=token,
            expires_at=datetime.now(UTC) + timedelta(days=30),
        )

        return self.session_repository.create(session)

    def register(self, data: RegisterRequest) -> User:
        email = str(data.email).lower()

        if self.user_repository.get_by_email(email):
            raise HTTPException(
                status_code=409,
                detail="Email already exists",
            )

        if self.user_repository.get_by_login(data.login):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Login already exists",
            )

        password_hash = PasswordService.hash_password(
            data.password
        )

        user = User(
            email=email,
            login=data.login,
            name=data.name,
            password_hash=password_hash,
            role=data.role,
        )

        return self.user_repository.create(user)

    def logout(
            self,
            session_token: str,
    ) -> None:
        session = self.session_repository.get_by_token(session_token)

        if session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        self.session_repository.delete(session)