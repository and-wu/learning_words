from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateWordRequest(BaseModel):
    korean: str
    translation: str
    part_of_speech: str | None = None
    comment: str | None = None

class UpdateWordRequest(BaseModel):
    korean: str | None = None
    translation: str | None = None
    part_of_speech: str | None = None
    comment: str | None = None

class WordResponse(BaseModel):
    id: int
    korean: str
    translation: str
    part_of_speech: str | None
    comment: str | None
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )