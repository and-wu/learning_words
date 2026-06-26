from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)

    auth_service = AuthService(user_repository)

    user = auth_service.register(data)

    return {
        "id": user.id,
        "email": user.email,
        "login": user.login,
    }