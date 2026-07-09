from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_exercise_service
from app.models import User
from app.schemas.exercises import (
    ExerciseResultResponse,
    SubmitExerciseRequest,
)
from app.services.exercise_service import ExerciseService

router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"],
)

@router.post("/submit", response_model=ExerciseResultResponse, status_code=status.HTTP_201_CREATED)
def submit_answer(
    data: SubmitExerciseRequest,
    current_user: User = Depends(get_current_user),
    exercise_service: ExerciseService = Depends(get_exercise_service),
):

    return exercise_service.submit_answer(
        current_user=current_user,
        data=data,
    )