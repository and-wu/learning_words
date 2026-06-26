from pydantic import BaseModel, ConfigDict

from app.enums.user_role import UserRole


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    login: str
    name: str
    role: UserRole