from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.teacher_student_repository import TeacherStudentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse
from app.services.teacher_student_service import TeacherStudentService

router = APIRouter(
    prefix="/teacher_students",
    tags=["Teacher Students"],
)

@router.get("/students", response_model=list[UserResponse])
def get_students(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)
    teacher_student_repository = TeacherStudentRepository(db)

    service = TeacherStudentService(
        user_repository=user_repository,
        teacher_student_repository=teacher_student_repository,
    )

    return service.get_students(current_user)

@router.get("/teachers", response_model=list[UserResponse])
def get_teachers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)
    teacher_student_repository = TeacherStudentRepository(db)

    service = TeacherStudentService(
        user_repository=user_repository,
        teacher_student_repository=teacher_student_repository,
    )

    return service.get_teachers(current_user)