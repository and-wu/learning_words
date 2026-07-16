from fastapi import HTTPException, status

from app.models import TeacherStudents
from app.models.user import User
from app.repositories.teacher_student_repository import TeacherStudentRepository
from app.repositories.user_repository import UserRepository


class TeacherStudentService:

    def __init__(
        self,
        user_repository: UserRepository,
        teacher_student_repository: TeacherStudentRepository,
    ):
        self.user_repository = user_repository
        self.teacher_student_repository = teacher_student_repository

    # ==========================================================
    # Public methods
    # ==========================================================

    # Возвращает список учеников текущего преподавателя
    def get_students(self, current_user: User) -> list[User]:

        return self.teacher_student_repository.get_student_users(
            current_user.id,
        )

    # Возвращает список преподавателей текущего ученика
    def get_teachers(self, current_user: User) -> list[User]:

        return self.teacher_student_repository.get_teacher_users(
            student_id=current_user.id,
        )

    # Деактивирует связь преподавателя и ученика
    def deactivate(self, current_user: User, relationship_id: int) -> None:

        relationship = self._get_relationship(relationship_id)

        self._validate_can_deactivate(
            current_user=current_user,
            relationship=relationship,
        )

        relationship.is_active = False

        self.teacher_student_repository.update(
            relationship,
        )

    # ==========================================================
    # Private methods
    # ==========================================================

    # Возвращает связь преподавателя и ученика либо выбрасывает 404
    def _get_relationship( self, relationship_id: int) -> TeacherStudents:

        relationship = self.teacher_student_repository.get_by_id(
            relationship_id,
        )

        if relationship is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relationship not found",
            )

        return relationship

    # Проверяет возможность деактивации связи
    def _validate_can_deactivate(self, current_user: User, relationship: TeacherStudents) -> None:

        # Связь уже отключена
        if not relationship.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Relationship is already inactive",
            )

        # Пользователь должен быть участником связи
        if (
                relationship.teacher_id != current_user.id
                and relationship.student_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot deactivate this relationship",
            )