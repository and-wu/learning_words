from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.teacher_students import TeacherStudents


class TeacherStudentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, teacher_student: TeacherStudents) -> TeacherStudents:

        self.db.add(teacher_student)
        self.db.flush()
        self.db.commit()
        self.db.refresh(teacher_student)

        return teacher_student

    def get_by_users(self, teacher_id: int, student_id: int) -> TeacherStudents | None:

        stmt = (
            select(TeacherStudents)
            .where(
                TeacherStudents.teacher_id == teacher_id,
                TeacherStudents.student_id == student_id,
            )
        )

        return self.db.scalar(stmt)

    def get_student_relationships(self, teacher_id: int, ) -> list[TeacherStudents]:
        stmt = (
            select(TeacherStudents)

            .where(
                TeacherStudents.teacher_id == teacher_id,
                TeacherStudents.is_active.is_(True),
            )
        )

        return self.db.scalars(stmt).all()

    # Возвращает пользователей-учеников конкретного преподавателя
    def get_student_users(self, teacher_id: int) -> list[User]:
        stmt = (
            select(User)
            .join(User.student_relationships)
            .where(
                TeacherStudents.teacher_id == teacher_id,
                TeacherStudents.is_active.is_(True),
            )
        )

        return self.db.scalars(stmt).all()

    # Возвращает пользователей-преподавателей конкретного ученика
    def get_teacher_users(self, student_id: int) -> list[User]:
        stmt = (
            select(User)
            .join(User.teacher_relationships)
            .where(
                TeacherStudents.student_id == student_id,
                TeacherStudents.is_active.is_(True),
            )
            .order_by(User.name)
        )

        return self.db.scalars(stmt).all()

    def get_teacher_relationships(self, student_id: int) -> list[TeacherStudents]:
        stmt = (
            select(TeacherStudents)
            .where(
                TeacherStudents.student_id == student_id,
                TeacherStudents.is_active.is_(True),
            )
        )

        return list(self.db.scalars(stmt))

    def get_by_id(self, relationship_id: int) -> TeacherStudents | None:
        stmt = (
            select(TeacherStudents)
            .where(
                TeacherStudents.id == relationship_id,
            )
        )

        return self.db.scalar(stmt)

    def update(self, relationship: TeacherStudents) -> TeacherStudents:
        self.db.add(relationship)
        self.db.flush()
        self.db.commit()
        self.db.refresh(relationship)

        return relationship

    # Проверяет, является ли преподаватель наставником ученика
    def is_teacher_of_student(self, teacher_id: int, student_id: int) -> bool:
        stmt = (
            select(TeacherStudents.id)
            .where(
                TeacherStudents.teacher_id == teacher_id,
                TeacherStudents.student_id == student_id,
                TeacherStudents.is_active.is_(True),
            )
            .limit(1)
        )

        return self.db.scalar(stmt) is not None

