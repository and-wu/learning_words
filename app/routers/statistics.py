from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_student_statistics_service
from app.models.user import User
from app.schemas.statistics import StudentStatisticsResponse
from app.services.student_statistics_service import StudentStatisticsService

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"],
)

# Возвращает статистику текущего ученика
@router.get(
    "",
    response_model=StudentStatisticsResponse,
)
def get_statistics(
    current_user: User = Depends(get_current_user),
    statistics_service: StudentStatisticsService = Depends(
        get_student_statistics_service,
    ),
):

    return statistics_service.get_statistics(
        current_user=current_user,
    )