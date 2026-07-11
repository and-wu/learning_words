from pydantic import BaseModel


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