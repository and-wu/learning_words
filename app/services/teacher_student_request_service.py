from app.repositories.teacher_student_repository import TeacherStudentRepository
from app.repositories.teacher_student_request_repository import (
    TeacherStudentRequestRepository,
)
from app.repositories.user_repository import UserRepository

from fastapi import HTTPException, status

from app.enums.request_status import RequestStatus
from app.enums.request_type import RequestType
from app.enums.user_role import UserRole
from app.models.teacher_student_requests import TeacherStudentRequests
from app.models.user import User
from app.schemas.teacher_student_request import (
    CreateTeacherStudentRequest,
)

class TeacherStudentRequestService:

    def __init__(
        self,
        user_repository: UserRepository,
        teacher_student_repository: TeacherStudentRepository,
        teacher_student_request_repository: TeacherStudentRequestRepository,
    ):
        self.user_repository = user_repository
        self.teacher_student_repository = teacher_student_repository
        self.teacher_student_request_repository = teacher_student_request_repository

    def create(self, current_user: User,
            data: CreateTeacherStudentRequest,
    ) -> TeacherStudentRequests:

        if current_user.id == data.to_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot send a request to yourself",
            )

        target_user = self.user_repository.get_by_id(
            data.to_user_id,
        )

        if target_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if data.request_type == RequestType.TEACHER_TO_STUDENT:
            if current_user.role != UserRole.teacher:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only teachers can send this request",
                )

            if target_user.role != UserRole.student:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Target user must be a student",
                )

        elif data.request_type == RequestType.STUDENT_TO_TEACHER:
            if current_user.role != UserRole.student:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only students can send this request",
                )

            if target_user.role != UserRole.teacher:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Target user must be a teacher",
                )


        if data.request_type == RequestType.TEACHER_TO_STUDENT:
            teacher_id = current_user.id
            student_id = target_user.id
        else:
            teacher_id = target_user.id
            student_id = current_user.id


        if self.teacher_student_repository.exists(
                teacher_id=teacher_id,
                student_id=student_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Teacher-student relationship already exists",
            )

        pending_request = self.teacher_student_request_repository.get_pending(
            from_user_id=current_user.id,
            to_user_id=target_user.id,
        )

        if pending_request is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Pending request already exists",
            )

        request = TeacherStudentRequests(
            from_user_id=current_user.id,
            to_user_id=target_user.id,
            request_type=data.request_type,
            status=RequestStatus.PENDING,
        )

        return self.teacher_student_request_repository.create(request)







