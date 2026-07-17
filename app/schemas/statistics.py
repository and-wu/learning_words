from pydantic import BaseModel, Field


class StudentStatisticsResponse(BaseModel):
    total_words: int = Field(ge=0)
    due_words: int = Field(ge=0)

    total_answers: int = Field(ge=0)
    correct_answers: int = Field(ge=0)
    wrong_answers: int = Field(ge=0)

    accuracy: float = Field(ge=0, le=100)

    current_streak: int = Field(ge=0)