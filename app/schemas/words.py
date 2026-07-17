from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreateWordRequest(BaseModel):
    korean: str = Field(
        min_length=1,
        max_length=100,
    )

    translation: str = Field(
        min_length=1,
        max_length=255,
    )

    part_of_speech: str | None = Field(
        default=None,
        max_length=50,
    )

    comment: str | None = Field(
        default=None,
        max_length=1000,
    )

class UpdateWordRequest(BaseModel):
    korean: str | None = Field(
        default=None,
        max_length=100,
    )
    translation: str = Field(
        min_length=1,
        max_length=255,
    )

    part_of_speech: str | None = Field(
        default=None,
        max_length=50,
    )

    comment: str | None = Field(
        default=None,
        max_length=1000,
    )

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