from pydantic import BaseModel, Field

from app.enums.exercise_type import ExerciseType


class NextExerciseResponse(BaseModel):
    student_word_id: int = Field(
        gt=0,
        description="Student word identifier",
    )

    exercise_type: ExerciseType = Field(
        description="Exercise type",
    )

    question: str = Field(
        min_length=1,
        description="Exercise question",
    )

    options: list[str] | None = Field(
        default=None,
        description="Answer options for multiple-choice exercises",
    )



