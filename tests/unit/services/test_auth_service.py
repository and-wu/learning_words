from unittest.mock import patch
from datetime import UTC, datetime, timedelta

import pytest
from fastapi import HTTPException

from app.enums.user_role import UserRole
from app.models.session import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import AuthService


class FakeUserRepository:

    def __init__(self, user: User | None = None):
        self.user = user
        self.created_user: User | None = None

    def get_by_login(self, login: str) -> User | None:
        users = [self.user, self.created_user]

        for user in users:
            if user is not None and user.login == login:
                return user

        return None

    def get_by_email(self, email: str) -> User | None:
        users = [self.user, self.created_user]

        for user in users:
            if user is not None and user.email == email:
                return user

        return None

    def create(self, user: User) -> User:
        self.created_user = user

        return user



class FakeSessionRepository:

    def __init__(self, session: Session | None = None):
        self.session = session
        self.created_session: Session | None = None
        self.deleted_session: Session | None = None

    def create(self, session: Session) -> Session:
        self.created_session = session

        return session

    def get_by_token(
            self,
            session_token: str,
    ) -> Session | None:
        if (
                self.session is not None
                and self.session.session_token == session_token
        ):
            return self.session

        return None

    def delete(self, session: Session) -> None:
        self.deleted_session = session


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
def empty_user_repository() -> FakeUserRepository:

    return FakeUserRepository()

@pytest.fixture
def session_repository() -> FakeSessionRepository:

    return FakeSessionRepository()

@pytest.fixture
def session() -> Session:

    return Session(
        id=1,
        user_id=1,
        session_token="valid-token",
        expires_at=datetime.now(UTC) + timedelta(days=30),
    )

@pytest.fixture
def service(
        user_repository: FakeUserRepository,
        session_repository: FakeSessionRepository) -> AuthService:

    return AuthService(user_repository=user_repository,
                       session_repository=session_repository)

@pytest.fixture
def registration_service(
    empty_user_repository: FakeUserRepository,
    session_repository: FakeSessionRepository,
) -> AuthService:

    return AuthService(user_repository=empty_user_repository,
                       session_repository=session_repository)

@pytest.fixture
def logout_service(
    session: Session,
) -> tuple[AuthService, FakeSessionRepository]:

    session_repository = FakeSessionRepository(
        session=session,
    )

    service = AuthService(
        user_repository=None,
        session_repository=session_repository,
    )

    return service, session_repository

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

# тест для проверки регистрации
@patch(
    "app.services.auth_service.PasswordService.hash_password",
    return_value="hashed_password",
)
def test_register_creates_user(
    mock_hash_password,
    registration_service: AuthService,
    empty_user_repository: FakeUserRepository
):
    data = RegisterRequest(
        email="STUDENT@EXAMPLE.COM",
        login="student",
        name="Student",
        password="password123",
        role=UserRole.STUDENT,
    )

    user = registration_service.register(data)

    assert user is empty_user_repository.created_user

    assert user.email == "student@example.com"

    assert user.login == "student"

    assert user.name == "Student"

    assert user.password_hash == "hashed_password"

    assert user.role == UserRole.STUDENT

    mock_hash_password.assert_called_once_with(
        "password123",
    )

#тест на проверку регистрации с уже существующем email
def test_register_with_existing_email_raises_409(
    service: AuthService,
    user_repository: FakeUserRepository,
):
    data = RegisterRequest(
        email="STUDENT@EXAMPLE.COM",
        login="new_student",
        name="New Student",
        password="password123",
        role=UserRole.STUDENT,
    )

    with pytest.raises(HTTPException) as exception:
        service.register(data)

    assert exception.value.status_code == 409

    assert exception.value.detail == "Email already exists"

    assert user_repository.created_user is None

#тест на проверку регистрации с уже существующем login
def test_register_with_existing_login_raises_409(
    service: AuthService,
    user_repository: FakeUserRepository,
):
    data = RegisterRequest(
        email="new@example.com",
        login="student",
        name="New Student",
        password="password123",
        role=UserRole.STUDENT,
    )

    with pytest.raises(HTTPException) as exception:
        service.register(data)

    assert exception.value.status_code == 409

    assert exception.value.detail == "Login already exists"

    assert user_repository.created_user is None

# тест успешного logout
def test_logout_deletes_existing_session(
    logout_service: tuple[
        AuthService,
        FakeSessionRepository,
    ],
    session: Session,
):
    service, session_repository = logout_service

    service.logout(
        session_token="valid-token",
    )

    assert session_repository.deleted_session is session

# тест logout с неизвестным токеном
def test_logout_with_unknown_token_raises_401():

    session_repository = FakeSessionRepository()

    service = AuthService(
        user_repository=None,
        session_repository=session_repository,
    )

    with pytest.raises(HTTPException) as exception:

        service.logout(
            session_token="unknown-token",
        )

    assert exception.value.status_code == 401

    assert exception.value.detail == "Not authenticated"

    assert session_repository.deleted_session is None