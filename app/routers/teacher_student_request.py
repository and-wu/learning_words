from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_teacher_student_request_service
from app.models.user import User
from app.schemas.teacher_student_request import CreateTeacherStudentRequest
from app.services.teacher_student_request_service import TeacherStudentRequestService

router = APIRouter(
    prefix="/teacher-student-requests",
    tags=["Teacher Student Requests"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create teacher/student request",
)
def create_request(
    data: CreateTeacherStudentRequest,
    current_user: User = Depends(get_current_user),
    service: TeacherStudentRequestService = Depends(
        get_teacher_student_request_service,
    ),
):
    return service.create(
        current_user=current_user,
        data=data,
    )


@router.get(
    "/incoming",
    status_code=status.HTTP_200_OK,
    summary="Get incoming requests",
)
def incoming(
    current_user: User = Depends(get_current_user),
    service: TeacherStudentRequestService = Depends(
        get_teacher_student_request_service,
    ),
):
    return service.get_incoming(
        current_user=current_user,
    )


@router.get(
    "/outgoing",
    status_code=status.HTTP_200_OK,
    summary="Get outgoing requests",
)
def outgoing(
    current_user: User = Depends(get_current_user),
    service: TeacherStudentRequestService = Depends(
        get_teacher_student_request_service,
    ),
):
    return service.get_outgoing(
        current_user=current_user,
    )


@router.patch(
    "/{request_id}/accept",
    status_code=status.HTTP_200_OK,
    summary="Accept request",
)
def accept(
    request_id: int,
    current_user: User = Depends(get_current_user),
    service: TeacherStudentRequestService = Depends(
        get_teacher_student_request_service,
    ),
):
    service.accept(
        current_user=current_user,
        request_id=request_id,
    )

    return {
        "message": "Request accepted",
    }


@router.patch(
    "/{request_id}/reject",
    status_code=status.HTTP_200_OK,
    summary="Reject request",
)
def reject(
    request_id: int,
    current_user: User = Depends(get_current_user),
    service: TeacherStudentRequestService = Depends(
        get_teacher_student_request_service,
    ),
):
    service.reject(
        current_user=current_user,
        request_id=request_id,
    )

    return {
        "message": "Request rejected",
    }