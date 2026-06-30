from pydantic import BaseModel

from app.enums.request_type import RequestType



class CreateTeacherStudentRequest(BaseModel):
    to_user_id: int
    request_type: RequestType

