from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.enums.exercise_type import ExerciseType

class SubmitExerciseRequest(BaseModel):
    student_word_id: int = Field(gt=0)
    exercise_type: ExerciseType
    response: str = Field(
        min_length=1,
        max_length=255,
    )

class ExerciseResultResponse(BaseModel):
    id: int
    user_id: int
    word_id: int
    exercise_type: ExerciseType
    correct: bool
    response: str | None = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )