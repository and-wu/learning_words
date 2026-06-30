from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database.session import get_db
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
def register(data: RegisterRequest,db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    session_repository = SessionRepository(db)

    auth_service = AuthService(user_repository=user_repository,
                               session_repository=session_repository)

    return auth_service.register(data)

@router.post("/login")
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    session_repository = SessionRepository(db)

    auth_service = AuthService(user_repository=user_repository,
                               session_repository=session_repository)

    session = auth_service.login(data)

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