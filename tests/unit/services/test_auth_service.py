from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.enums.user_role import UserRole
from app.models.session import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest
from app.services.auth_service import AuthService


class FakeUserRepository:

    def __init__(self, user: User):
        self.user = user

    def get_by_login(self, login: str) -> User | None:
        if login == self.user.login:
            return self.user

        return None


class FakeSessionRepository:

    def __init__(self):
        self.created_session: Session | None = None

    def create(self, session: Session) -> Session:
        self.created_session = session

        return session

@pytest.fixture
def user() -> User:

    return User(
        id=1,
        email="student@example.com",
        login="student",
        name="Student",
        password_hash="hashed_password",
        role=UserRole.STUDENT,
    )

@pytest.fixture
def user_repository(user: User) -> FakeUserRepository:

    return FakeUserRepository(user)

@pytest.fixture
def session_repository() -> FakeSessionRepository:

    return FakeSessionRepository()

@pytest.fixture
def service(
        user_repository: UserRepository,
        session_repository: FakeSessionRepository) -> AuthService:

    return AuthService(user_repository=user_repository,
                       session_repository=session_repository)


# тест на правильный пароль
@patch(
    "app.services.auth_service.PasswordService.verify_password",
    return_value=True,
)
def test_login_with_valid_credentials_creates_session(
    mock_verify_password,
    service: AuthService,
    user: User,
    session_repository: FakeSessionRepository,
):

    session = service.login(
        data=LoginRequest(
            login="student",
            password="password123",
        ),
    )

    assert session is not None

    assert session.user_id == user.id

    assert session.session_token is not None

    assert session.expires_at is not None

    assert session_repository.created_session is session

    mock_verify_password.assert_called_once_with(
        "password123",
        "hashed_password",
    )

# тест на неправильный пароль
@patch(
    "app.services.auth_service.PasswordService.verify_password",
    return_value=False,
)
def test_login_with_invalid_password_raises_401(
    mock_verify_password,
    service: AuthService,
    session_repository: FakeSessionRepository,
):

    with pytest.raises(HTTPException) as exception:

        service.login(
            data=LoginRequest(
                login="student",
                password="wrong_password",
            ),
        )

    assert exception.value.status_code == 401

    assert exception.value.detail == "Invalid login or password"

    assert session_repository.created_session is None

    mock_verify_password.assert_called_once_with(
        "wrong_password",
        "hashed_password",
    )

# тест на ненайденного пользователя
def test_login_with_unknown_login_raises_401(
        service: AuthService,
        session_repository: FakeSessionRepository,
):

    with pytest.raises(HTTPException) as exception:

        service.login(
            data=LoginRequest(
                login="unknown",
                password="password123",
            ),
        )

    assert exception.value.status_code == 401

    assert exception.value.detail == "Invalid login or password"

    assert session_repository.created_session is None