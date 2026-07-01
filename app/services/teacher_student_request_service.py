from datetime import datetime, UTC

from app.repositories.teacher_student_repository import TeacherStudentRepository
from app.repositories.teacher_student_request_repository import (
    TeacherStudentRequestRepository,
)
from app.repositories.user_repository import UserRepository

from fastapi import HTTPException, status

from app.enums.request_status import RequestStatus
from app.enums.request_type import RequestType
from app.enums.user_role import UserRole
from app.models.teacher_student_requests import TeacherStudentRequest
from app.models.user import User
from app.models.teacher_students import TeacherStudents
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
    ) -> TeacherStudentRequest:

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

        pending_request = (
            self.teacher_student_request_repository.get_pending_between_users(
                user1_id=current_user.id,
                user2_id=target_user.id,
            )
        )

        if pending_request is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Pending request already exists",
            )

        request = TeacherStudentRequest(
            from_user_id=current_user.id,
            to_user_id=target_user.id,
            request_type=data.request_type,
            status=RequestStatus.PENDING,
        )

        return self.teacher_student_request_repository.create(request)

    def get_incoming(
        self,
        current_user: User,
    ) -> list[TeacherStudentRequest]:

        return self.teacher_student_request_repository.get_incoming(current_user.id)

    def get_outgoing(
        self,
        current_user: User,
    ) -> list[TeacherStudentRequest]:

        return self.teacher_student_request_repository.get_outgoing(current_user.id)


    def accept(self, current_user: User, request_id: int) -> None:

        request = self.teacher_student_request_repository.get_by_id(request_id)

        if request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        if request.status != RequestStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request has already been processed",
            )

        if request.to_user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot accept this request",
            )

        if request.request_type == RequestType.TEACHER_TO_STUDENT:
            teacher_id = request.from_user_id
            student_id = request.to_user_id
        else:
            teacher_id = request.to_user_id
            student_id = request.from_user_id

        if self.teacher_student_repository.exists(
                teacher_id=teacher_id,
                student_id=student_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Relationship already exists",
            )

        relationship = TeacherStudents(
            teacher_id=teacher_id,
            student_id=student_id,
        )

        self.teacher_student_repository.create(
            relationship,
        )

        request.status = RequestStatus.ACCEPTED
        request.processed_at = datetime.now(UTC)

        self.teacher_student_request_repository.update(request)

    def reject(self, current_user: User, request_id: int) -> None:

        request = self.teacher_student_request_repository.get_by_id(request_id)

        if request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        if request.status != RequestStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request has already been processed",
            )

        if request.to_user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot reject this request",
            )

        request.status = RequestStatus.REJECTED
        request.processed_at = datetime.now(UTC)

        self.teacher_student_request_repository.update(request)




