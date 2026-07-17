from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_teacher_dashboard_service
from app.models.user import User
from app.schemas.teacher_dashboard import (
    StudentDashboardDetailsResponse,
    StudentDashboardResponse,
    StudentHistoryResponse,
)
from app.services.teacher_dashboard_service import TeacherDashboardService

router = APIRouter(
    prefix="/teachers/dashboard",
    tags=["Teacher Dashboard"],
)


@router.get(
    "",
    response_model=list[StudentDashboardResponse],
    status_code=status.HTTP_200_OK,
    summary="Get teacher dashboard",
)
def get_students_dashboard(
    current_user: User = Depends(get_current_user),
    service: TeacherDashboardService = Depends(
        get_teacher_dashboard_service,
    ),
):
    return service.get_students_dashboard(
        current_user=current_user,
    )


@router.get(
    "/students/{student_id}",
    response_model=StudentDashboardDetailsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get student dashboard",
)
def get_student_dashboard(
    student_id: int,
    current_user: User = Depends(get_current_user),
    service: TeacherDashboardService = Depends(
        get_teacher_dashboard_service,
    ),
):
    return service.get_student_dashboard(
        current_user=current_user,
        student_id=student_id,
    )


@router.get(
    "/students/{student_id}/history",
    response_model=StudentHistoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get student exercise history",
)
def get_student_history(
    student_id: int,
    current_user: User = Depends(get_current_user),
    service: TeacherDashboardService = Depends(
        get_teacher_dashboard_service,
    ),
):
    return service.get_student_history(
        current_user=current_user,
        student_id=student_id,
    )