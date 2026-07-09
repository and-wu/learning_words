from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_teacher_student_service
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
    service: TeacherStudentService = Depends(
        get_teacher_student_service,
    )
):

    return service.get_students(current_user)

@router.get("/teachers", response_model=list[UserResponse])
def get_teachers(
    current_user: User = Depends(get_current_user),
    service: TeacherStudentService = Depends(
        get_teacher_student_service,
    ),
):

    return service.get_teachers(current_user)

@router.patch("/{relationship_id}/deactivate")
def deactivate(
    relationship_id: int,
    current_user: User = Depends(get_current_user),
    service: TeacherStudentService = Depends(
        get_teacher_student_service,
    ),
):

    service.deactivate(
        current_user=current_user,
        relationship_id=relationship_id,
    )

    return {
        "message": "Relationship deactivated",
    }