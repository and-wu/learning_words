from fastapi import HTTPException, status

from app.enums.source_type import SourceType
from app.enums.user_role import UserRole
from app.models import StudentWord, User
from app.repositories.student_words_repository import StudentWordRepository
from app.repositories.teacher_student_repository import TeacherStudentRepository
from app.repositories.user_repository import UserRepository
from app.repositories.word_repository import WordRepository


class StudentWordService:

    def __init__(
        self,
        user_repository: UserRepository,
        word_repository: WordRepository,
        teacher_student_repository: TeacherStudentRepository,
        student_word_repository: StudentWordRepository,
    ):
        self.user_repository = user_repository
        self.word_repository = word_repository
        self.teacher_student_repository = teacher_student_repository
        self.student_word_repository = student_word_repository

    def assign_by_teacher(self, teacher: User, student_id: int, word_id: int) -> StudentWord:

        if teacher.role != UserRole.teacher:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only teachers can assign words",
            )

        student = self.user_repository.get_by_id(student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found",
            )

        if student.role != UserRole.student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a student",
            )

        relationship = self.teacher_student_repository.get_by_users(
            teacher_id=teacher.id,
            student_id=student.id,
        )

        if relationship is None or not relationship.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Teacher and student are not connected",
            )

        word = self.word_repository.get_by_id(word_id)

        if word is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Word not found",
            )

        if self.student_word_repository.exists(
                student_id=student.id,
                word_id=word.id,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Word already assigned",
            )

        student_word = StudentWord(
            student_id=student.id,
            word_id=word.id,
            assigned_by=teacher.id,
            source_type=SourceType.TEACHER,
        )

        return self.student_word_repository.create(student_word)

    def assign_to_self(self, student: User, word_id: int) -> StudentWord:

        if student.role != UserRole.student:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can add words",
            )

        word = self.word_repository.get_by_id(word_id)

        if word is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Word not found",
            )

        if self.student_word_repository.exists(
                student_id=student.id,
                word_id=word.id,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Word already added",
            )

        student_word = StudentWord(
            student_id=student.id,
            word_id=word.id,
            assigned_by=student.id,
            source_type=SourceType.SELF,
        )

        return self.student_word_repository.create(student_word)

    def get_student_words(self, current_user: User) -> list[StudentWord]:

        if current_user.role != UserRole.student:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can view their words",
            )

        return self.student_word_repository.get_student_words(
            student_id=current_user.id,
        )

    def remove(self, current_user: User, student_word_id: int) -> None:

        student_word = self.student_word_repository.get_by_id(
            student_word_id,
        )

        if student_word is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student word not found",
            )

        if (
                current_user.id != student_word.student_id
                and current_user.id != student_word.assigned_by
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot remove this word",
            )

        if (
                current_user.role == UserRole.teacher
                and student_word.source_type != SourceType.TEACHER
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Teacher cannot remove student's own word",
            )

        self.student_word_repository.delete(student_word)