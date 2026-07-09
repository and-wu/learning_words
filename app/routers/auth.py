from fastapi import APIRouter, Depends, Response, Cookie
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.services import get_auth_service
from app.models.user import User
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest, LoginRequest
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register", response_model=UserResponse)
def register(data: RegisterRequest, service: AuthService = Depends(get_auth_service)):

    return service.register(data)

@router.post("/login")
def login(data: LoginRequest, response: Response, service: AuthService = Depends(get_auth_service)):

    session = service.login(data)

    response.set_cookie(
        key="session_token",
        value=session.session_token,
        httponly=True,
        max_age=60 * 60 * 24 * 30,
    )

    return {
        "message": "Login successful",
    }

@router.get("/me",response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
def logout(
    response: Response,
    session_token: str | None = Cookie(default=None),
    service: AuthService = Depends(get_auth_service),
):

    service.logout(session_token)

    response.delete_cookie("session_token")

    return {
        "message": "Logout successful",
    }


