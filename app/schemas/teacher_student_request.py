from pydantic import BaseModel, Field

from app.enums.request_type import RequestType



class CreateTeacherStudentRequest(BaseModel):
    to_user_id: int = Field(gt=0)
    request_type: RequestType

