from datetime import datetime

from pydantic import BaseModel

from app.enums.exercise_type import ExerciseType


class StudentDashboardResponse(BaseModel):
    student_id: int
    name: str
    email: str
    total_words: int
    due_words: int
    total_answers: int
    correct_answers: int
    accuracy: float
    current_streak: int

class StudentWordProgressResponse(BaseModel):
    student_word_id: int
    word_id: int
    korean: str
    translation: str
    correct_streak: int
    wrong_count: int
    interval_days: int
    last_review_at: datetime | None
    next_review_at: datetime | None

class StudentDashboardDetailsResponse(BaseModel):
    student_id: int
    name: str
    email: str
    words: list[StudentWordProgressResponse]

class ExerciseHistoryResponse(BaseModel):
    korean: str
    translation: str
    exercise_type: ExerciseType
    correct: bool
    response: str
    created_at: datetime

class StudentHistoryResponse(BaseModel):
    student_id: int
    student_name: str
    history: list[ExerciseHistoryResponse]