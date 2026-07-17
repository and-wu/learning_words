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

    # Создает новую заявку на связь между преподавателем и учеником
    def create(self, current_user: User,
            data: CreateTeacherStudentRequest,
    ) -> TeacherStudentRequest:

        # Получаем пользователя, которому отправляется заявка
        target_user = self._get_target_user(current_user=current_user,
                                            to_user_id=data.to_user_id)

        # Проверяем соответствие ролей типу заявки
        self._validate_roles(
            current_user=current_user,
            target_user=target_user,
            request_type=data.request_type,
        )

        # Определяем преподавателя и ученика
        teacher_id, student_id = self._resolve_users(
            current_user=current_user,
            target_user=target_user,
            request_type=data.request_type,
        )

        # Проверяем, что связь уже не существует
        self._validate_relationship(
            teacher_id=teacher_id,
            student_id=student_id,
        )

        # Проверяем отсутствие активной заявки
        self._validate_pending_request(
            from_user_id=current_user.id,
            to_user_id=target_user.id,
        )

        # Создаем новую заявку
        return self.teacher_student_request_repository.create(
            TeacherStudentRequest(
                from_user_id=current_user.id,
                to_user_id=target_user.id,
                request_type=data.request_type,
                status=RequestStatus.PENDING,
            )
        )

    # Возвращает входящие заявки пользователя
    def get_incoming(
        self,
        current_user: User,
    ) -> list[TeacherStudentRequest]:

        return self.teacher_student_request_repository.get_incoming(current_user.id)

    # Возвращает исходящие заявки пользователя
    def get_outgoing(
        self,
        current_user: User,
    ) -> list[TeacherStudentRequest]:

        return self.teacher_student_request_repository.get_outgoing(current_user.id)

    # Принимает заявку и создает связь преподаватель–ученик
    def accept(self, current_user: User, request_id: int) -> None:

        request = self._get_pending_request(
            current_user=current_user,
            request_id=request_id,
        )

        teacher_id, student_id = self._resolve_users_from_request(request)

        relationship = self.teacher_student_repository.get_by_users(
            teacher_id=teacher_id,
            student_id=student_id,
        )

        # Если связи еще нет — создаем
        if relationship is None:

            self.teacher_student_repository.create(
                TeacherStudents(
                    teacher_id=teacher_id,
                    student_id=student_id,
                )
            )

        # Если связь была отключена — активируем снова
        elif not relationship.is_active:

            relationship.is_active = True

            self.teacher_student_repository.update(
                relationship,
            )

        # Помечаем заявку как принятую
        request.status = RequestStatus.ACCEPTED
        request.processed_at = datetime.now(UTC)

        self.teacher_student_request_repository.update(request)

    # Отклоняет заявку
    def reject(self, current_user: User, request_id: int) -> None:

        request = self._get_pending_request(
            current_user=current_user,
            request_id=request_id,
        )

        request.status = RequestStatus.REJECTED
        request.processed_at = datetime.now(UTC)

        self.teacher_student_request_repository.update(request)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    # Получает пользователя-получателя заявки
    def _get_target_user(
        self,
        current_user: User,
        to_user_id: int,
    ) -> User:

        if current_user.id == to_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot send a request to yourself",
            )

        user = self.user_repository.get_by_id(to_user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    # Проверяет корректность ролей участников заявки
    def _validate_roles(
        self,
        current_user: User,
        target_user: User,
        request_type: RequestType,
    ) -> None:

        if request_type == RequestType.TEACHER_TO_STUDENT:

            if current_user.role != UserRole.TEACHER:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only teachers can send this request",
                )

            if target_user.role != UserRole.STUDENT:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Target user must be a student",
                )

        else:

            if current_user.role != UserRole.STUDENT:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only students can send this request",
                )

            if target_user.role != UserRole.TEACHER:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Target user must be a teacher",
                )

    # Определяет id преподавателя и ученика
    def _resolve_users(
        self,
        current_user: User,
        target_user: User,
        request_type: RequestType,
    ) -> tuple[int, int]:

        if request_type == RequestType.TEACHER_TO_STUDENT:
            return current_user.id, target_user.id

        return target_user.id, current_user.id

    # Проверяет существование активной связи
    def _validate_relationship(
        self,
        teacher_id: int,
        student_id: int,
    ) -> None:

        relationship = self.teacher_student_repository.get_by_users(
            teacher_id=teacher_id,
            student_id=student_id,
        )

        if relationship is not None and relationship.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Relationship already exists",
            )

    # Проверяет отсутствие активной заявки
    def _validate_pending_request(
        self,
        from_user_id: int,
        to_user_id: int,
    ) -> None:

        pending = self.teacher_student_request_repository.get_pending_between_users(
            user1_id=from_user_id,
            user2_id=to_user_id,
        )

        if pending is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Pending request already exists",
            )

    # Получает заявку и проверяет возможность обработки
    def _get_pending_request(
        self,
        current_user: User,
        request_id: int,
    ) -> TeacherStudentRequest:

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
                detail="You cannot process this request",
            )

        return request

    # Определяет преподавателя и ученика по заявке
    def _resolve_users_from_request(
        self,
        request: TeacherStudentRequest,
    ) -> tuple[int, int]:

        if request.request_type == RequestType.TEACHER_TO_STUDENT:
            return request.from_user_id, request.to_user_id

        return request.to_user_id, request.from_user_id


