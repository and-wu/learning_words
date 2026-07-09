from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.exercise_type import ExerciseType

class SubmitExerciseRequest(BaseModel):
    student_word_id: int
    exercise_type: ExerciseType
    response: str

class ExerciseResultResponse(BaseModel):
    id: int
    user_id: int
    word_id: int
    exercise_type: ExerciseType
    correct: bool
    response: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )