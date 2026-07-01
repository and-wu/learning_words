
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories import teacher_student_request_repository
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

@router.get("/incoming")
def incoming(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    user_repository = UserRepository(db=db)
    teacher_student_repository = TeacherStudentRepository(db=db)
    teacher_student_request_repository = TeacherStudentRequestRepository(db=db)

    service = TeacherStudentRequestService(user_repository=user_repository,
                                           teacher_student_repository=teacher_student_repository,
                                           teacher_student_request_repository=teacher_student_request_repository)

    return service.get_incoming(current_user=current_user)

@router.get("/outgoing")
def outgoing(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    user_repository = UserRepository(db=db)
    teacher_student_repository = TeacherStudentRepository(db=db)
    teacher_student_request_repository = TeacherStudentRequestRepository(db=db)

    service = TeacherStudentRequestService(user_repository=user_repository,
                                           teacher_student_repository=teacher_student_repository,
                                           teacher_student_request_repository=teacher_student_request_repository)

    return service.get_outgoing(current_user=current_user)


@router.post("/{request_id}/accept")
def accept(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)
    teacher_student_repository = TeacherStudentRepository(db)
    teacher_student_request_repository = TeacherStudentRequestRepository(db)

    service = TeacherStudentRequestService(
        user_repository=user_repository,
        teacher_student_repository=teacher_student_repository,
        teacher_student_request_repository=teacher_student_request_repository,
    )

    service.accept(
        current_user=current_user,
        request_id=request_id,
    )

    return {
        "message": "Request accepted",
    }

@router.post("/{request_id}/reject")
def reject(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)
    teacher_student_repository = TeacherStudentRepository(db)
    teacher_student_request_repository = TeacherStudentRequestRepository(db)

    service = TeacherStudentRequestService(
        user_repository=user_repository,
        teacher_student_repository=teacher_student_repository,
        teacher_student_request_repository=teacher_student_request_repository,
    )

    service.reject(
        current_user=current_user,
        request_id=request_id,
    )

    return {
        "message": "Request rejected",
    }