
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.teacher_student_repository import TeacherStudentRepository
from app.repositories.teacher_student_request_repository import (
    TeacherStudentRequestRepository,
)
from app.repositories.user_repository import UserRepository
from app.schemas.teacher_student_request import (
    CreateTeacherStudentRequest,
)
from app.services.teacher_student_request_service import (
    TeacherStudentRequestService,
)

router = APIRouter(
    prefix="/teacher-student-requests",
    tags=["Teacher Student Requests"],
)

@router.post("")
def create_request(
    data: CreateTeacherStudentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user_repository = UserRepository(db=db)
    teacher_student_repository = TeacherStudentRepository(db=db)
    teacher_student_request_repository = TeacherStudentRequestRepository(db=db)

    service = TeacherStudentRequestService(user_repository=user_repository,
                                           teacher_student_repository=teacher_student_repository,
                                           teacher_student_request_repository=teacher_student_request_repository)


    return service.create(current_user=current_user, data=data)



