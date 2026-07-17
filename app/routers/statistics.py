from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_student_statistics_service
from app.models.user import User
from app.schemas.statistics import StudentStatisticsResponse
from app.services.student_statistics_service import StudentStatisticsService

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"],
)


@router.get(
    "",
    response_model=StudentStatisticsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current student statistics",
)
def get_statistics(
    current_user: User = Depends(get_current_user),
    service: StudentStatisticsService = Depends(
        get_student_statistics_service,
    ),
):
    return service.get_statistics(
        current_user=current_user,
    )