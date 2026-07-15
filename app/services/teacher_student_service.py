from fastapi import HTTPException, status

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


    def get_students(self, current_user: User) -> list[User]:

        relationships = self.teacher_student_repository.get_students(teacher_id=current_user.id)

        students = []

        for relationship in relationships:
            student = self.user_repository.get_by_id(
                relationship.student_id,
            )

            if student is not None:
                students.append(student)

        return students

    def get_teachers(self, current_user: User) -> list[User]:

        relationships = self.teacher_student_repository.get_teacher_relationships(
            student_id=current_user.id,
        )

        teachers = []

        for relationship in relationships:
            teacher = self.user_repository.get_by_id(
                relationship.teacher_id,
            )

            if teacher is not None:
                teachers.append(teacher)

        return teachers

    def deactivate(
            self,
            current_user: User,
            relationship_id: int,
    ) -> None:

        relationship = self.teacher_student_repository.get_by_id(
            relationship_id,
        )

        if relationship is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relationship not found",
            )

        if not relationship.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Relationship is already inactive",
            )

        if (
                relationship.teacher_id != current_user.id
                and relationship.student_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot deactivate this relationship",
            )

        relationship.is_active = False

        self.teacher_student_repository.update(
            relationship,
        )