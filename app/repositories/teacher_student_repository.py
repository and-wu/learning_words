from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.teacher_students import TeacherStudents


class TeacherStudentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, teacher_student: TeacherStudents) -> TeacherStudents:
        self.db.add(teacher_student)
        self.db.commit()
        self.db.refresh(teacher_student)

        return teacher_student

    def exists(self, teacher_id: int, student_id: int) -> bool:
        stmt = (
            select(TeacherStudents)
            .where(
                TeacherStudents.teacher_id == teacher_id,
                TeacherStudents.student_id == student_id,
            )
        )

        teacher_student = self.db.scalar(stmt)

        return teacher_student is not None

    def get_students(self, teacher_id: int, ) -> list[TeacherStudents]:
        stmt = (
            select(TeacherStudents)
            .where(
                TeacherStudents.teacher_id == teacher_id,
                TeacherStudents.is_active.is_(True),
            )
        )

        return self.db.scalars(stmt).all()

    def get_teachers(self, student_id: int) -> list[TeacherStudents]:
        stmt = (
            select(TeacherStudents)
            .where(
                TeacherStudents.student_id == student_id,
                TeacherStudents.is_active.is_(True),
            )
        )

        return list(self.db.scalars(stmt))

