from pydantic import BaseModel


class StudentStatisticsResponse(BaseModel):
    total_words: int
    due_words: int

    total_answers: int
    correct_answers: int
    wrong_answers: int

    accuracy: float

    current_streak: int