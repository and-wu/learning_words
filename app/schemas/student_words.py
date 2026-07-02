from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.source_type import SourceType


class AssignWordRequest(BaseModel):
    student_id: int
    word_id: int


class SelfAssignWordRequest(BaseModel):
    word_id: int


class StudentWordResponse(BaseModel):
    id: int
    student_id: int
    word_id: int
    assigned_by: int | None
    source_type: SourceType
    correct_streak: int
    wrong_count: int
    last_result: bool | None
    last_review_at: datetime | None
    next_review_at: datetime
    interval_days: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )