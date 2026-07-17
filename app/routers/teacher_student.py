from fastapi import APIRouter, Depends, Response, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_teacher_student_service
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.teacher_student_service import TeacherStudentService

router = APIRouter(
    prefix="/teacher-students",
    tags=["Teacher Students"],
)


@router.get(
    "/students",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get teacher students",
)
def get_students(
    current_user: User = Depends(get_current_user),
    service: TeacherStudentService = Depends(get_teacher_student_service),
):
    return service.get_students(current_user)


@router.get(
    "/teachers",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get student teachers",
)
def get_teachers(
    current_user: User = Depends(get_current_user),
    service: TeacherStudentService = Depends(get_teacher_student_service),
):
    return service.get_teachers(current_user)


@router.patch(
    "/{relationship_id}/deactivate",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deactivate teacher-student relationship",
)
def deactivate(
    relationship_id: int,
    current_user: User = Depends(get_current_user),
    service: TeacherStudentService = Depends(get_teacher_student_service),
):
    service.deactivate(
        current_user=current_user,
        relationship_id=relationship_id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)