from pydantic import BaseModel, EmailStr, Field, field_validator

from app.enums.user_role import UserRole


class RegisterRequest(BaseModel):
    email: EmailStr
    login: str = Field(min_length=3, max_length=50)
    name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8)
    role: UserRole

    @field_validator("email", mode="after")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).lower()

class LoginRequest(BaseModel):
    login: str
    password: str