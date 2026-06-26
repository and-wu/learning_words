from app.enums.user_role import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest
from app.services.password_service import PasswordService

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, data: RegisterRequest) -> User:
        email = str(data.email).lower()

        if self.user_repository.get_by_email(email):
            raise ValueError("Email already exists")

        if self.user_repository.get_by_login(data.login):
            raise ValueError("Login already exists")

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