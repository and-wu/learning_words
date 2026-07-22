from datetime import datetime

from pydantic import BaseModel, Field

from app.enums.exercise_type import ExerciseType


class StudentDashboardResponse(BaseModel):
    student_id: int = Field(gt=0)
    name: str
    email: str
    total_words: int = Field(ge=0)
    due_words: int = Field(ge=0)
    total_answers: int = Field(ge=0)
    correct_answers: int = Field(ge=0)
    accuracy: float = Field(ge=0, le=100)
    current_streak: int = Field(ge=0)

class StudentWordProgressResponse(BaseModel):
    student_word_id: int = Field(gt=0)
    word_id: int = Field(gt=0)
    korean: str
    translation: str
    correct_streak: int = Field(ge=0)
    wrong_count: int = Field(ge=0)
    interval_days: int = Field(ge=0)
    last_review_at: datetime | None
    next_review_at: datetime | None

class StudentDashboardDetailsResponse(BaseModel):
    student_id: int = Field(gt=0)
    name: str
    email: str
    words: list[StudentWordProgressResponse]

class ExerciseHistoryResponse(BaseModel):
    korean: str
    translation: str
    exercise_type: ExerciseType
    correct: bool
    response: str | None
    created_at: datetime

class StudentHistoryResponse(BaseModel):
    student_id: int = Field(gt=0)
    student_name: str
    history: list[ExerciseHistoryResponse]