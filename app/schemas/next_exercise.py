from pydantic import BaseModel

from app.enums.exercise_type import ExerciseType


class NextExerciseResponse(BaseModel):
    student_word_id: int
    exercise_type: ExerciseType
    question:str
    options: list[str] | None = None



